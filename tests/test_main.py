import tempfile
import unittest
from unittest.mock import mock_open, patch

from tfblocks import main


class TestResourceMatching(unittest.TestCase):
    def test_no_filters(self):
        """Test that resources match when no filters are specified"""
        self.assertTrue(main.is_resource_match("aws_s3_bucket.test", [], []))

    def test_address_filter_exact_match(self):
        """Test exact address filtering"""
        self.assertTrue(
            main.is_resource_match("aws_s3_bucket.test", ["aws_s3_bucket.test"], [])
        )
        self.assertFalse(
            main.is_resource_match("aws_s3_bucket.test", ["aws_s3_bucket.other"], [])
        )

    def test_indexed_resource_match(self):
        """Test matching with indexed resources"""
        self.assertTrue(
            main.is_resource_match("aws_s3_bucket.test[0]", ["aws_s3_bucket.test"], [])
        )
        self.assertTrue(
            main.is_resource_match(
                'aws_s3_bucket.test["name"]', ["aws_s3_bucket.test"], []
            )
        )

    def test_module_match(self):
        """Test matching resources in modules"""
        self.assertTrue(
            main.is_resource_match(
                "module.my_module.aws_s3_bucket.test", ["module.my_module"], []
            )
        )
        self.assertTrue(
            main.is_resource_match(
                "module.my_module[0].aws_s3_bucket.test", ["module.my_module"], []
            )
        )
        
    def test_resource_type_name_match(self):
        """Test matching resources by type and name across different module paths"""
        # Resource in a module should match the same resource type and name from a file
        self.assertTrue(
            main.is_resource_match(
                "module.my_module.aws_s3_bucket.test", [], ["aws_s3_bucket.test"]
            )
        )
        
        # Different resource name should not match
        self.assertFalse(
            main.is_resource_match(
                "module.my_module.aws_s3_bucket.test", [], ["aws_s3_bucket.other"]
            )
        )
        
        # Different resource type should not match
        self.assertFalse(
            main.is_resource_match(
                "module.my_module.aws_s3_bucket.test", [], ["aws_lambda_function.test"]
            )
        )

    def test_intersection_filter(self):
        """Test that both address and file filters must match"""
        self.assertTrue(
            main.is_resource_match(
                "aws_s3_bucket.test", ["aws_s3_bucket.test"], ["aws_s3_bucket.test"]
            )
        )
        self.assertFalse(
            main.is_resource_match(
                "aws_s3_bucket.test", ["aws_s3_bucket.test"], ["aws_s3_bucket.other"]
            )
        )


class TestFileProcessing(unittest.TestCase):
    def test_extract_resource_addresses_from_content(self):
        """Test extracting resource addresses from content"""
        terraform_content = """
        resource "aws_s3_bucket" "bucket" {
          bucket = "my-bucket"
        }

        resource "aws_dynamodb_table" "table" {
          name = "my-table"
        }

        module "vpc" {
          source = "./modules/vpc"
        }
        """

        addresses = main.extract_resource_addresses_from_content(terraform_content)

        self.assertEqual(len(addresses), 3)
        self.assertIn("aws_s3_bucket.bucket", addresses)
        self.assertIn("aws_dynamodb_table.table", addresses)
        self.assertIn("module.vpc", addresses)
        
    def test_file_exists(self):
        """Test file existence check"""
        # Test with tempfile to avoid dependencies on filesystem
        with tempfile.NamedTemporaryFile() as temp_file:
            self.assertTrue(main.file_exists(temp_file.name))
            
        # This path should not exist
        self.assertFalse(main.file_exists("/path/that/does/not/exist/file.tf"))
            
    def test_extract_resource_addresses_nonexistent_file(self):
        """Test behavior with nonexistent file"""
        with patch("tfblocks.main.file_exists", return_value=False), \
             patch("sys.exit") as mock_exit:
            main.extract_resource_addresses_from_file("nonexistent.tf")
            mock_exit.assert_called_once_with(1)

    def test_filter_resources_basic(self):
        """Test basic resource filtering without files"""
        # Create a test state
        test_state = {
            "values": {
                "root_module": {
                    "resources": [
                        {
                            "address": "aws_s3_bucket.included",
                            "type": "aws_s3_bucket",
                            "mode": "managed",
                            "values": {"bucket": "included-bucket"},
                        },
                        {
                            "address": "aws_s3_bucket.excluded",
                            "type": "aws_s3_bucket",
                            "mode": "managed",
                            "values": {"bucket": "excluded-bucket"},
                        },
                        {
                            "address": "aws_dynamodb_table.test",
                            "type": "aws_dynamodb_table",
                            "mode": "managed",
                            "values": {"name": "test-table"},
                        },
                    ],
                    "child_modules": [
                        {
                            "resources": [
                                {
                                    "address": "module.test.aws_s3_bucket.nested",
                                    "type": "aws_s3_bucket",
                                    "mode": "managed",
                                    "values": {"bucket": "nested-bucket"},
                                }
                            ]
                        }
                    ],
                }
            }
        }

        # Test with no filters
        resources = main.filter_resources(test_state)
        self.assertEqual(len(resources), 4)  # Should get all AWS resources

        # Test with address filters
        resources = main.filter_resources(test_state, ["aws_s3_bucket.included"])
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]["address"], "aws_s3_bucket.included")

        # Test with module filter
        resources = main.filter_resources(test_state, ["module.test"])
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]["address"], "module.test.aws_s3_bucket.nested")
        
    def test_filter_resources_with_file_filters(self):
        """Test resource filtering with file filters"""
        # Create a test state
        test_state = {
            "values": {
                "root_module": {
                    "resources": [
                        {
                            "address": "aws_s3_bucket.test",
                            "type": "aws_s3_bucket",
                            "mode": "managed",
                            "values": {"bucket": "test-bucket"},
                        }
                    ]
                }
            }
        }

        # Mock the file handling part without mocking implementation details
        with patch("tfblocks.main.extract_resource_addresses_from_file") as mock_extract:
            # Case 1: File contains matching resource
            mock_extract.return_value = ["aws_s3_bucket.test"]
            resources = main.filter_resources(test_state, [], ["matching_file.tf"])
            self.assertEqual(len(resources), 1)
            self.assertEqual(resources[0]["address"], "aws_s3_bucket.test")
            
            # Case 2: File contains non-matching resource
            mock_extract.return_value = ["aws_lambda_function.not_in_state"]
            resources = main.filter_resources(test_state, [], ["non_matching_file.tf"])
            self.assertEqual(len(resources), 0)


class TestBlockGeneration(unittest.TestCase):
    def test_generate_import_block(self):
        """Test generating an import block for a resource"""
        resource = {
            "address": "aws_s3_bucket.test",
            "type": "aws_s3_bucket",
            "values": {"bucket": "test-bucket"},
        }

        # Using a simplified schema_classes for testing
        schema_classes = {}

        block = main.generate_import_block(resource, schema_classes)
        self.assertIn("to = aws_s3_bucket.test", block)
        self.assertIn("id =", block)

    def test_generate_removed_block(self):
        """Test generating a removed block for a resource"""
        # Test with destroy=False (default)
        expected_block = """removed {
  from = aws_s3_bucket.test
  lifecycle {
    destroy = false
  }
}"""
        block = main.generate_removed_block("aws_s3_bucket.test[0]")
        self.assertEqual(block, expected_block)

        # Test with destroy=True
        expected_block_destroy = """removed {
  from = aws_s3_bucket.test
  lifecycle {
    destroy = true
  }
}"""
        block = main.generate_removed_block("aws_s3_bucket.test[0]", True)
        self.assertEqual(block, expected_block_destroy)

    def test_generate_blocks_for_command(self):
        """Test the generate_blocks_for_command function"""
        resources = [
            {
                "address": "aws_s3_bucket.test1",
                "type": "aws_s3_bucket",
                "values": {"bucket": "test-bucket-1"},
            },
            {
                "address": "aws_s3_bucket.test2[0]",
                "type": "aws_s3_bucket",
                "values": {"bucket": "test-bucket-2"},
            },
        ]

        # Test import blocks
        import_blocks = main.generate_blocks_for_command(resources, "import")
        self.assertEqual(len(import_blocks), 2)

        # Test removed blocks (should deduplicate aws_s3_bucket.test2)
        test2_resource = {
            "address": "aws_s3_bucket.test2[1]",  # Different index, same base address
            "type": "aws_s3_bucket",
            "values": {"bucket": "test-bucket-2-1"},
        }
        resources.append(test2_resource)

        removed_blocks = main.generate_blocks_for_command(resources, "remove")
        # Should have 2 blocks, not 3, due to deduplication
        self.assertEqual(len(removed_blocks), 2)


if __name__ == "__main__":
    unittest.main()
