import json
import typing as t


class BaseResource:
    def __init__(self, address: str, attributes: t.Dict[str, t.Any]):
        self.address = address
        self.attributes = attributes or {}

    @property
    def import_id(self) -> str | None:
        return self._get_import_id()

    def _get_import_id(self) -> str | None:
        return None

    def has_attributes(self, required_attributes: list[str]) -> bool:
        return all(attr in self.attributes for attr in required_attributes)


class AwsAccessanalyzerAnalyzer(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("analyzer_name", None)


class AwsAccessanalyzerArchiveRule(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["analyzer_name", "rule_name"]):
            return None
        return f"{self.attributes['analyzer_name']}/{self.attributes['rule_name']}"


class AwsAccountAlternateContact(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["alternate_contact_type"]):
            return None

        account_id = self.attributes.get("account_id", "")
        alternate_contact_type = self.attributes["alternate_contact_type"]

        return f"{account_id}/{alternate_contact_type}".strip("/")


class AwsAccountPrimaryContact(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("account_id") or self.attributes.get(
            "aws_account_id"
        )


class AwsAccountRegion(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["region_name"]):
            return None

        if "account_id" in self.attributes:
            return f"{self.attributes['account_id']},{self.attributes['region_name']}"

        return self.attributes["region_name"]


class AwsAcmCertificate(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsAcmpcaCertificate(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsAcmpcaCertificateAuthority(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsAcmpcaCertificateAuthorityCertificate(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["certificate_authority_arn"]):
            return None
        return self.attributes["certificate_authority_arn"]


class AwsAcmpcaPermission(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["certificate_authority_arn", "principal"]):
            return None
        return f"{self.attributes['certificate_authority_arn']}|{self.attributes['principal']}"


class AwsAcmpcaPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("resource_arn", None)


class AwsAmi(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsAmiCopy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsAmiFromInstance(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsAmiLaunchPermission(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["image_id"]):
            return None

        if self.attributes.get("account_id"):
            return f"{self.attributes['account_id']}/{self.attributes['image_id']}"

        if self.attributes.get("group"):
            return f"{self.attributes['group']}/{self.attributes['image_id']}"

        if self.attributes.get("organization_arn"):
            return (
                f"{self.attributes['organization_arn']}/{self.attributes['image_id']}"
            )

        if self.attributes.get("organizational_unit_arn"):
            return f"{self.attributes['organizational_unit_arn']}/{self.attributes['image_id']}"

        return None


class AwsAmplifyApp(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsAmplifyBackendEnvironment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["app_id", "environment_name"]):
            return None
        return f"{self.attributes['app_id']}/{self.attributes['environment_name']}"


class AwsAmplifyBranch(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["app_id", "branch_name"]):
            return None
        return f"{self.attributes['app_id']}/{self.attributes['branch_name']}"


class AwsAmplifyDomainAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["app_id", "domain_name"]):
            return None
        return f"{self.attributes['app_id']}/{self.attributes['domain_name']}"


class AwsAmplifyWebhook(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsApiGatewayAccount(BaseResource):
    def _get_import_id(self) -> str | None:
        return "api-gateway-account"


class AwsApiGatewayApiKey(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsApiGatewayAuthorizer(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["rest_api_id", "id"]):
            return None
        return f"{self.attributes['rest_api_id']}/{self.attributes['id']}"


class AwsApiGatewayBasePathMapping(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["domain_name"]):
            return None

        base_path = self.attributes.get("base_path", "")
        domain_name_id = self.attributes.get("domain_name_id", "")

        if domain_name_id:
            return (
                f"{self.attributes['domain_name']}/{base_path}/{domain_name_id}".rstrip(
                    "/"
                )
            )

        return f"{self.attributes['domain_name']}/{base_path}".rstrip("/")


class AwsApiGatewayClientCertificate(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsApiGatewayDeployment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["rest_api_id", "id"]):
            return None
        return f"{self.attributes['rest_api_id']}/{self.attributes['id']}"


class AwsApiGatewayDocumentationPart(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["rest_api_id", "documentation_part_id"]):
            return None
        return f"{self.attributes['rest_api_id']}/{self.attributes['documentation_part_id']}"


class AwsApiGatewayDocumentationVersion(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["rest_api_id", "version"]):
            return None
        return f"{self.attributes['rest_api_id']}/{self.attributes['version']}"


class AwsApiGatewayDomainName(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["domain_name"]):
            return None

        # Check if domain_name_id exists for private custom domain names
        if "domain_name_id" in self.attributes:
            return (
                f"{self.attributes['domain_name']}/{self.attributes['domain_name_id']}"
            )

        return self.attributes["domain_name"]


class AwsApiGatewayDomainNameAccessAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsApiGatewayGatewayResponse(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["rest_api_id", "response_type"]):
            return None
        return f"{self.attributes['rest_api_id']}/{self.attributes['response_type']}"


class AwsApiGatewayIntegration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["rest_api_id", "resource_id", "http_method"]):
            return None
        return f"{self.attributes['rest_api_id']}/{self.attributes['resource_id']}/{self.attributes['http_method']}"


class AwsApiGatewayIntegrationResponse(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = ["rest_api_id", "resource_id", "http_method", "status_code"]
        if not self.has_attributes(required_attrs):
            return None
        return f"{self.attributes['rest_api_id']}/{self.attributes['resource_id']}/{self.attributes['http_method']}/{self.attributes['status_code']}"


class AwsApiGatewayMethod(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["rest_api_id", "resource_id", "http_method"]):
            return None
        return f"{self.attributes['rest_api_id']}/{self.attributes['resource_id']}/{self.attributes['http_method']}"


class AwsApiGatewayMethodResponse(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = ["rest_api_id", "resource_id", "http_method", "status_code"]
        if not self.has_attributes(required_attrs):
            return None
        return f"{self.attributes['rest_api_id']}/{self.attributes['resource_id']}/{self.attributes['http_method']}/{self.attributes['status_code']}"


class AwsApiGatewayMethodSettings(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["rest_api_id", "stage_name", "method_path"]):
            return None
        return f"{self.attributes['rest_api_id']}/{self.attributes['stage_name']}/{self.attributes['method_path']}"


class AwsApiGatewayModel(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["rest_api_id", "name"]):
            return None
        return f"{self.attributes['rest_api_id']}/{self.attributes['name']}"


class AwsApiGatewayRequestValidator(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["rest_api_id", "id"]):
            return None
        return f"{self.attributes['rest_api_id']}/{self.attributes['id']}"


class AwsApiGatewayResource(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["rest_api_id", "id"]):
            return None
        return f"{self.attributes['rest_api_id']}/{self.attributes['id']}"


class AwsApiGatewayRestApi(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsApiGatewayRestApiPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["rest_api_id"]):
            return None
        return self.attributes["rest_api_id"]


class AwsApiGatewayStage(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["rest_api_id", "stage_name"]):
            return None
        return f"{self.attributes['rest_api_id']}/{self.attributes['stage_name']}"


class AwsApiGatewayUsagePlan(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsApiGatewayUsagePlanKey(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["usage_plan_id", "id"]):
            return None
        return f"{self.attributes['usage_plan_id']}/{self.attributes['id']}"


class AwsApiGatewayVpcLink(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsApigatewayv2Api(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsApigatewayv2ApiMapping(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id", "domain_name"]):
            return None
        return f"{self.attributes['id']}/{self.attributes['domain_name']}"


class AwsApigatewayv2Authorizer(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["api_id", "id"]):
            return None
        return f"{self.attributes['api_id']}/{self.attributes['id']}"


class AwsApigatewayv2Deployment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["api_id", "id"]):
            return None
        return f"{self.attributes['api_id']}/{self.attributes['id']}"


class AwsApigatewayv2DomainName(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("domain_name", None)


class AwsApigatewayv2Integration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["api_id", "id"]):
            return None
        return f"{self.attributes['api_id']}/{self.attributes['id']}"


class AwsApigatewayv2IntegrationResponse(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["api_id", "integration_id", "id"]):
            return None
        return f"{self.attributes['api_id']}/{self.attributes['integration_id']}/{self.attributes['id']}"


class AwsApigatewayv2Model(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["api_id", "id"]):
            return None
        return f"{self.attributes['api_id']}/{self.attributes['id']}"


class AwsApigatewayv2Route(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["api_id", "id"]):
            return None
        return f"{self.attributes['api_id']}/{self.attributes['id']}"


class AwsApigatewayv2RouteResponse(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["api_id", "route_id", "id"]):
            return None
        return f"{self.attributes['api_id']}/{self.attributes['route_id']}/{self.attributes['id']}"


class AwsApigatewayv2Stage(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["api_id", "name"]):
            return None
        return f"{self.attributes['api_id']}/{self.attributes['name']}"


class AwsApigatewayv2VpcLink(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsAppautoscalingPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = [
            "service_namespace",
            "resource_id",
            "scalable_dimension",
            "name",
        ]
        if not self.has_attributes(required_attrs):
            return None

        return f"{self.attributes['service_namespace']}/{self.attributes['resource_id']}/{self.attributes['scalable_dimension']}/{self.attributes['name']}"


class AwsAppautoscalingScheduledAction(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = [
            "name",
            "service_namespace",
            "resource_id",
            "scalable_dimension",
        ]
        if not self.has_attributes(required_attrs):
            return None

        return f"{self.attributes['service_namespace']}/{self.attributes['resource_id']}/{self.attributes['scalable_dimension']}/{self.attributes['name']}"


class AwsAppautoscalingTarget(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = ["service_namespace", "resource_id", "scalable_dimension"]
        if not self.has_attributes(required_attrs):
            return None
        return f"{self.attributes['service_namespace']}/{self.attributes['resource_id']}/{self.attributes['scalable_dimension']}"


class AwsAppconfigApplication(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsAppconfigConfigurationProfile(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["application_id", "configuration_profile_id"]):
            return None
        return f"{self.attributes['configuration_profile_id']}:{self.attributes['application_id']}"


class AwsAppconfigDeployment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(
            ["application_id", "environment_id", "deployment_number"]
        ):
            return None
        return f"{self.attributes['application_id']}/{self.attributes['environment_id']}/{self.attributes['deployment_number']}"


class AwsAppconfigDeploymentStrategy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsAppconfigEnvironment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["application_id", "environment_id"]):
            return None
        return (
            f"{self.attributes['environment_id']}:{self.attributes['application_id']}"
        )


class AwsAppconfigExtension(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsAppconfigExtensionAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsAppconfigHostedConfigurationVersion(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(
            ["application_id", "configuration_profile_id", "version_number"]
        ):
            return None
        return f"{self.attributes['application_id']}/{self.attributes['configuration_profile_id']}/{self.attributes['version_number']}"


class AwsAppfabricAppAuthorization(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsAppfabricAppAuthorizationConnection(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["app_authorization_arn", "app_bundle_arn"]):
            return None
        return f"{self.attributes['app_authorization_arn']}/{self.attributes['app_bundle_arn']}"


class AwsAppfabricAppBundle(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsAppfabricIngestion(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["app_bundle_arn", "arn"]):
            return None
        return f"{self.attributes['app_bundle_arn']},{self.attributes['arn']}"


class AwsAppfabricIngestionDestination(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsAppflowConnectorProfile(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsAppflowFlow(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsAppintegrationsDataIntegration(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsAppintegrationsEventIntegration(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsApplicationinsightsApplication(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("resource_group_name", None)


class AwsAppmeshGatewayRoute(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["mesh_name", "virtual_gateway_name", "name"]):
            return None

        mesh_name = self.attributes["mesh_name"]
        virtual_gateway_name = self.attributes["virtual_gateway_name"]
        name = self.attributes["name"]

        return f"{mesh_name}/{virtual_gateway_name}/{name}"


class AwsAppmeshMesh(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsAppmeshRoute(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = ["mesh_name", "virtual_router_name", "name"]
        if not self.has_attributes(required_attrs):
            return None

        mesh_name = self.attributes["mesh_name"]
        virtual_router_name = self.attributes["virtual_router_name"]
        route_name = self.attributes["name"]

        return f"{mesh_name}/{virtual_router_name}/{route_name}"


class AwsAppmeshVirtualGateway(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["mesh_name", "name"]):
            return None
        return f"{self.attributes['mesh_name']}/{self.attributes['name']}"


class AwsAppmeshVirtualNode(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name", "mesh_name"]):
            return None

        mesh_name = self.attributes["mesh_name"]
        name = self.attributes["name"]

        return f"{mesh_name}/{name}"


class AwsAppmeshVirtualRouter(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["mesh_name", "name"]):
            return None
        return f"{self.attributes['mesh_name']}/{self.attributes['name']}"


class AwsAppmeshVirtualService(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["mesh_name", "name"]):
            return None
        return f"{self.attributes['mesh_name']}/{self.attributes['name']}"


class AwsApprunnerAutoScalingConfigurationVersion(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsApprunnerConnection(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("connection_name", None)


class AwsApprunnerCustomDomainAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["domain_name", "service_arn"]):
            return None
        return f"{self.attributes['domain_name']},{self.attributes['service_arn']}"


class AwsApprunnerDefaultAutoScalingConfigurationVersion(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["auto_scaling_configuration_arn"]):
            return None
        region = self.attributes["auto_scaling_configuration_arn"].split(":")[3]
        return region


class AwsApprunnerDeployment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["service_arn", "operation_id"]):
            return None
        return f"{self.attributes['service_arn']}/{self.attributes['operation_id']}"


class AwsApprunnerObservabilityConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsApprunnerService(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsApprunnerVpcConnector(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsApprunnerVpcIngressConnection(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsAppstreamDirectoryConfig(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("directory_name", None)


class AwsAppstreamFleet(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsAppstreamFleetStackAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["fleet_name", "stack_name"]):
            return None
        return f"{self.attributes['fleet_name']}/{self.attributes['stack_name']}"


class AwsAppstreamImageBuilder(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsAppstreamStack(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsAppstreamUser(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["user_name", "authentication_type"]):
            return None
        return (
            f"{self.attributes['user_name']}/{self.attributes['authentication_type']}"
        )


class AwsAppstreamUserStackAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["user_name", "authentication_type", "stack_name"]):
            return None
        return f"{self.attributes['user_name']}/{self.attributes['authentication_type']}/{self.attributes['stack_name']}"


class AwsAppsyncApiCache(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("api_id", None)


class AwsAppsyncApiKey(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["api_id", "key"]):
            return None
        return f"{self.attributes['api_id']}:{self.attributes['key']}"


class AwsAppsyncDatasource(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["api_id", "name"]):
            return None
        return f"{self.attributes['api_id']}-{self.attributes['name']}"


class AwsAppsyncDomainName(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("domain_name", None)


class AwsAppsyncDomainNameApiAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("domain_name", None)


class AwsAppsyncFunction(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["api_id", "function_id"]):
            return None
        return f"{self.attributes['api_id']}-{self.attributes['function_id']}"


class AwsAppsyncGraphqlApi(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsAppsyncResolver(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["api_id", "type", "field"]):
            return None
        return f"{self.attributes['api_id']}-{self.attributes['type']}-{self.attributes['field']}"


class AwsAppsyncSourceApiAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["merged_api_id", "association_id"]):
            return None
        return f"{self.attributes['merged_api_id']},{self.attributes['association_id']}"


class AwsAppsyncType(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["api_id", "format", "name"]):
            return None
        return f"{self.attributes['api_id']}:{self.attributes['format']}:{self.attributes['name']}"


class AwsAthenaNamedQuery(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsAthenaPreparedStatement(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name", "workgroup"]):
            return None
        return f"{self.attributes['workgroup']}/{self.attributes['name']}"


class AwsAthenaWorkgroup(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsAuditmanagerAccountRegistration(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsAuditmanagerAssessment(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsAuditmanagerAssessmentDelegation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["assessment_id", "role_arn", "control_set_id"]):
            return None
        return f"{self.attributes['assessment_id']},{self.attributes['role_arn']},{self.attributes['control_set_id']}"


class AwsAuditmanagerAssessmentReport(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsAuditmanagerControl(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsAuditmanagerFramework(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsAuditmanagerFrameworkShare(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsAuditmanagerOrganizationAdminAccountRegistration(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("admin_account_id", None)


class AwsAutoscalingAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["autoscaling_group_name"]):
            return None

        if self.has_attributes(["elb"]):
            return (
                f"{self.attributes['autoscaling_group_name']}/{self.attributes['elb']}"
            )

        if self.has_attributes(["lb_target_group_arn"]):
            return f"{self.attributes['autoscaling_group_name']}/{self.attributes['lb_target_group_arn']}"

        return None


class AwsAutoscalingGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsAutoscalingGroupTag(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["autoscaling_group_name", "tag"]):
            return None
        tag_key = self.attributes["tag"][0]["key"]
        return f"{self.attributes['autoscaling_group_name']},{tag_key}"


class AwsAutoscalingLifecycleHook(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name", "autoscaling_group_name"]):
            return None
        return f"{self.attributes['autoscaling_group_name']}/{self.attributes['name']}"


class AwsAutoscalingNotification(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["group_names", "topic_arn"]):
            return None
        return f"{self.attributes['topic_arn']}:{','.join(sorted(self.attributes['group_names']))}"


class AwsAutoscalingPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name", "autoscaling_group_name"]):
            return None
        return f"{self.attributes['autoscaling_group_name']}/{self.attributes['name']}"


class AwsAutoscalingSchedule(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["autoscaling_group_name", "scheduled_action_name"]):
            return None
        return f"{self.attributes['autoscaling_group_name']}/{self.attributes['scheduled_action_name']}"


class AwsAutoscalingTrafficSourceAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["autoscaling_group_name", "traffic_source"]):
            return None

        traffic_source = self.attributes["traffic_source"][0]
        return f"{self.attributes['autoscaling_group_name']}/{traffic_source['identifier']}"


class AwsAutoscalingplansScalingPlan(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsBackupFramework(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsBackupGlobalSettings(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsBackupLogicallyAirGappedVault(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsBackupPlan(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsBackupRegionSettings(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id")


class AwsBackupReportPlan(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsBackupRestoreTestingPlan(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsBackupRestoreTestingSelection(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name", "restore_testing_plan_name"]):
            return None
        return (
            f"{self.attributes['name']}:{self.attributes['restore_testing_plan_name']}"
        )


class AwsBackupSelection(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["plan_id", "id"]):
            return None
        return f"{self.attributes['plan_id']}|{self.attributes['id']}"


class AwsBackupVault(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsBackupVaultLockConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("backup_vault_name", None)


class AwsBackupVaultNotifications(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["backup_vault_name"]):
            return None
        return self.attributes["backup_vault_name"]


class AwsBackupVaultPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("backup_vault_name", None)


class AwsBatchComputeEnvironment(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("compute_environment_name", None)


class AwsBatchJobDefinition(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsBatchJobQueue(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsBatchSchedulingPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsBcmdataexportsExport(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["export_arn"]):
            return None
        return self.attributes["export_arn"]


class AwsBedrockCustomModel(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["job_arn"]):
            return None
        return self.attributes["job_arn"]


class AwsBedrockGuardrail(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["guardrail_id", "version"]):
            return None
        return f"{self.attributes['guardrail_id']},{self.attributes['version']}"


class AwsBedrockGuardrailVersion(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["guardrail_arn", "version"]):
            return None
        return f"{self.attributes['guardrail_arn']},{self.attributes['version']}"


class AwsBedrockInferenceProfile(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsBedrockModelInvocationLoggingConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsBedrockProvisionedModelThroughput(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("provisioned_model_arn", None)


class AwsBedrockagentAgent(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("agent_id", None)


class AwsBedrockagentAgentActionGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["action_group_id", "agent_id", "agent_version"]):
            return None
        return f"{self.attributes['action_group_id']},{self.attributes['agent_id']},{self.attributes['agent_version']}"


class AwsBedrockagentAgentAlias(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["agent_alias_id", "agent_id"]):
            return None
        return f"{self.attributes['agent_alias_id']},{self.attributes['agent_id']}"


class AwsBedrockagentAgentCollaborator(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["agent_id", "agent_version", "collaborator_id"]):
            return None
        return f"{self.attributes['agent_id']},{self.attributes['agent_version']},{self.attributes['collaborator_id']}"


class AwsBedrockagentAgentKnowledgeBaseAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["agent_id", "knowledge_base_id"]):
            return None
        agent_version = self.attributes.get("agent_version", "DRAFT")
        return f"{self.attributes['agent_id']},{agent_version},{self.attributes['knowledge_base_id']}"


class AwsBedrockagentDataSource(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["data_source_id", "knowledge_base_id"]):
            return None
        return f"{self.attributes['data_source_id']},{self.attributes['knowledge_base_id']}"


class AwsBedrockagentKnowledgeBase(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsBudgetsBudget(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name", "account_id"]):
            return None
        account_id = self.attributes.get("account_id") or self.attributes.get(
            "aws_account_id"
        )
        budget_name = self.attributes.get("name")
        return f"{account_id}:{budget_name}"


class AwsBudgetsBudgetAction(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["account_id", "action_id", "budget_name"]):
            return None

        account_id = self.attributes.get("account_id", "")
        action_id = self.attributes.get("action_id", "")
        budget_name = self.attributes.get("budget_name", "")

        return f"{account_id}:{action_id}:{budget_name}"


class AwsCeAnomalyMonitor(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsCeAnomalySubscription(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsCeCostAllocationTag(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("tag_key", None)


class AwsCeCostCategory(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsChatbotSlackChannelConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["chat_configuration_arn"]):
            return None
        return self.attributes["chat_configuration_arn"]


class AwsChatbotTeamsChannelConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["team_id"]):
            return None
        return self.attributes["team_id"]


class AwsChimeVoiceConnector(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsChimeVoiceConnectorGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsChimeVoiceConnectorLogging(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["voice_connector_id"]):
            return None
        return self.attributes["voice_connector_id"]


class AwsChimeVoiceConnectorOrigination(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["voice_connector_id"]):
            return None
        return self.attributes["voice_connector_id"]


class AwsChimeVoiceConnectorStreaming(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["voice_connector_id"]):
            return None
        return self.attributes["voice_connector_id"]


class AwsChimeVoiceConnectorTermination(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["voice_connector_id"]):
            return None
        return self.attributes["voice_connector_id"]


class AwsChimeVoiceConnectorTerminationCredentials(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("voice_connector_id", None)


class AwsChimesdkmediapipelinesMediaInsightsPipelineConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsChimesdkvoiceGlobalSettings(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsChimesdkvoiceSipMediaApplication(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsChimesdkvoiceSipRule(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsChimesdkvoiceVoiceProfileDomain(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsCleanroomsCollaboration(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsCleanroomsConfiguredTable(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsCleanroomsMembership(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsCloud9EnvironmentEc2(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsCloud9EnvironmentMembership(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["environment_id", "user_arn"]):
            return None
        return f"{self.attributes['environment_id']}#{self.attributes['user_arn']}"


class AwsCloudcontrolapiResource(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["type_name", "desired_state"]):
            return None
        desired_state = json.loads(self.attributes["desired_state"])
        cluster_name = desired_state.get("ClusterName")
        return (
            f"{self.attributes['type_name']}:{cluster_name}" if cluster_name else None
        )


class AwsCloudformationStack(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsCloudformationStackInstances(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["stack_set_name"]):
            return None

        call_as = self.attributes.get("call_as", "SELF")

        # Check if this is an OU-based deployment
        if self.attributes.get("deployment_targets", {}).get("organizational_unit_ids"):
            return f"{self.attributes['stack_set_name']},{call_as},OU"

        return f"{self.attributes['stack_set_name']},{call_as}"


class AwsCloudformationStackSet(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None

        call_as = self.attributes.get("call_as", "SELF")

        if call_as == "DELEGATED_ADMIN":
            return f"{self.attributes['name']},{call_as}"

        return self.attributes["name"]


class AwsCloudformationStackSetInstance(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["stack_set_name", "region"]):
            return None

        # Handle account-based import
        if "account_id" in self.attributes:
            return f"{self.attributes['stack_set_name']},{self.attributes['account_id']},{self.attributes['region']}"

        # Handle organizational unit-based import
        if (
            "deployment_targets" in self.attributes
            and "organizational_unit_ids" in self.attributes["deployment_targets"]
        ):
            ou_ids = "/".join(
                self.attributes["deployment_targets"]["organizational_unit_ids"]
            )
            return f"{self.attributes['stack_set_name']},{ou_ids},{self.attributes['region']}"

        # Handle delegated admin scenario
        if (
            "call_as" in self.attributes
            and self.attributes["call_as"] == "DELEGATED_ADMIN"
        ):
            if "account_id" in self.attributes:
                return f"{self.attributes['stack_set_name']},{self.attributes['account_id']},{self.attributes['region']},DELEGATED_ADMIN"
            elif (
                "deployment_targets" in self.attributes
                and "organizational_unit_ids" in self.attributes["deployment_targets"]
            ):
                ou_ids = "/".join(
                    self.attributes["deployment_targets"]["organizational_unit_ids"]
                )
                return f"{self.attributes['stack_set_name']},{ou_ids},{self.attributes['region']},DELEGATED_ADMIN"

        return None


class AwsCloudformationType(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["type_arn", "version_id"]):
            return None
        return f"{self.attributes['type_arn']}/{self.attributes['version_id']}"


class AwsCloudfrontkeyvaluestoreKey(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["key_value_store_arn", "key"]):
            return None
        return f"{self.attributes['key_value_store_arn']},{self.attributes['key']}"


class AwsCloudtrail(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsCloudtrailEventDataStore(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsCloudtrailOrganizationDelegatedAdminAccount(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["account_id"]):
            return None
        return self.attributes["account_id"]


class AwsCloudwatchCompositeAlarm(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("alarm_name", None)


class AwsCloudwatchDashboard(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("dashboard_name", None)


class AwsCloudwatchEventApiDestination(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsCloudwatchEventArchive(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsCloudwatchEventBus(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsCloudwatchEventBusPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("event_bus_name", "default")


class AwsCloudwatchEventConnection(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsCloudwatchEventEndpoint(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsCloudwatchEventPermission(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["statement_id"]):
            return None
        event_bus_name = self.attributes.get("event_bus_name", "default")
        return f"{event_bus_name}/{self.attributes['statement_id']}"


class AwsCloudwatchEventRule(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None

        event_bus_name = self.attributes.get("event_bus_name", "default")
        return f"{event_bus_name}/{self.attributes['name']}"


class AwsCloudwatchEventTarget(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["rule", "target_id"]):
            return None

        event_bus_name = self.attributes.get("event_bus_name", "default")
        return (
            f"{event_bus_name}/{self.attributes['rule']}/{self.attributes['target_id']}"
        )


class AwsCloudwatchLogAccountPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["policy_name", "policy_type"]):
            return None
        return f"{self.attributes['policy_name']}:{self.attributes['policy_type']}"


class AwsCloudwatchLogAnomalyDetector(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsCloudwatchLogDataProtectionPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["log_group_name"]):
            return None
        return self.attributes["log_group_name"]


class AwsCloudwatchLogDelivery(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsCloudwatchLogDeliveryDestination(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsCloudwatchLogDeliveryDestinationPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("delivery_destination_name", None)


class AwsCloudwatchLogDeliverySource(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsCloudwatchLogDestination(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsCloudwatchLogDestinationPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("destination_name", None)


class AwsCloudwatchLogGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsCloudwatchLogIndexPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["log_group_name"]):
            return None
        return self.attributes["log_group_name"]


class AwsCloudwatchLogMetricFilter(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["log_group_name", "name"]):
            return None
        return f"{self.attributes['log_group_name']}:{self.attributes['name']}"


class AwsCloudwatchLogResourcePolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["policy_name"]):
            return None
        return self.attributes["policy_name"]


class AwsCloudwatchLogStream(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["log_group_name", "name"]):
            return None
        return f"{self.attributes['log_group_name']}:{self.attributes['name']}"


class AwsCloudwatchLogSubscriptionFilter(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name", "log_group_name"]):
            return None
        return f"{self.attributes['log_group_name']}|{self.attributes['name']}"


class AwsCloudwatchMetricAlarm(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["alarm_name"]):
            return None
        return self.attributes["alarm_name"]


class AwsCloudwatchMetricStream(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsCloudwatchQueryDefinition(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("query_definition_id", None)


class AwsCodeartifactDomain(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsCodeartifactRepository(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsCodeartifactRepositoryPermissionsPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["resource_arn"]):
            return None
        return self.attributes["resource_arn"]


class AwsCodebuildFleet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsCodebuildProject(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsCodebuildReportGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsCodebuildResourcePolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("resource_arn", None)


class AwsCodebuildSourceCredential(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsCodebuildWebhook(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["project_name"]):
            return None
        return self.attributes["project_name"]


class AwsCodecatalystDevEnvironment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["space_name", "project_name", "id"]):
            return None
        return f"{self.attributes['space_name']}/{self.attributes['project_name']}/{self.attributes['id']}"


class AwsCodecatalystProject(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsCodecatalystSourceRepository(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsCodecommitApprovalRuleTemplate(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsCodecommitApprovalRuleTemplateAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["approval_rule_template_name", "repository_name"]):
            return None
        return f"{self.attributes['approval_rule_template_name']},{self.attributes['repository_name']}"


class AwsCodecommitRepository(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["repository_name"]):
            return None
        return self.attributes["repository_name"]


class AwsCodecommitTrigger(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["repository_name", "configuration_id"]):
            return None
        return f"{self.attributes['repository_name']}:{self.attributes['configuration_id']}"


class AwsCodeconnectionsConnection(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsCodeconnectionsHost(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsCodedeployApp(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsCodedeployDeploymentConfig(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["deployment_config_name"]):
            return None
        return self.attributes["deployment_config_name"]


class AwsCodedeployDeploymentGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["app_name", "deployment_group_name"]):
            return None
        return (
            f"{self.attributes['app_name']}:{self.attributes['deployment_group_name']}"
        )


class AwsCodeguruprofilerProfilingGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsCodepipeline(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsCodepipelineCustomActionType(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["category", "provider_name", "version"]):
            return None
        return f"{self.attributes['category']}:{self.attributes['provider_name']}:{self.attributes['version']}"


class AwsCodepipelineWebhook(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsCodestarnotificationsNotificationRule(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsCognitoIdentityPool(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsCognitoIdentityPoolProviderPrincipalTag(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["identity_pool_id", "identity_provider_name"]):
            return None
        return f"{self.attributes['identity_pool_id']}:{self.attributes['identity_provider_name']}"


class AwsCognitoIdentityPoolRolesAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["identity_pool_id"]):
            return None
        return self.attributes["identity_pool_id"]


class AwsCognitoIdentityProvider(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["user_pool_id", "provider_name"]):
            return None
        return f"{self.attributes['user_pool_id']}:{self.attributes['provider_name']}"


class AwsCognitoManagedUserPoolClient(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["user_pool_id", "id"]):
            return None
        return f"{self.attributes['user_pool_id']}/{self.attributes['id']}"


class AwsCognitoResourceServer(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["user_pool_id", "identifier"]):
            return None
        return f"{self.attributes['user_pool_id']}|{self.attributes['identifier']}"


class AwsCognitoRiskConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["user_pool_id"]):
            return None

        if "client_id" in self.attributes:
            return f"{self.attributes['user_pool_id']}:{self.attributes['client_id']}"

        return self.attributes["user_pool_id"]


class AwsCognitoUser(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["user_pool_id", "username"]):
            return None
        return f"{self.attributes['user_pool_id']}/{self.attributes['username']}"


class AwsCognitoUserGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["user_pool_id", "name"]):
            return None
        return f"{self.attributes['user_pool_id']}/{self.attributes['name']}"


class AwsCognitoUserInGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["user_pool_id", "group_name", "username"]):
            return None
        return f"{self.attributes['user_pool_id']}|{self.attributes['group_name']}|{self.attributes['username']}"


class AwsCognitoUserPool(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsCognitoUserPoolClient(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["user_pool_id", "id"]):
            return None
        return f"{self.attributes['user_pool_id']}/{self.attributes['id']}"


class AwsCognitoUserPoolDomain(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["domain"]):
            return None
        return self.attributes["domain"]


class AwsCognitoUserPoolUiCustomization(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["user_pool_id", "client_id"]):
            return None
        return f"{self.attributes['user_pool_id']},{self.attributes['client_id']}"


class AwsComprehendDocumentClassifier(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsComprehendEntityRecognizer(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsConfigAggregateAuthorization(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["account_id", "region"]):
            return None
        return f"{self.attributes['account_id']}:{self.attributes['region']}"


class AwsConfigConfigRule(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsConfigConfigurationAggregator(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsConfigConfigurationRecorder(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsConfigConfigurationRecorderStatus(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsConfigConformancePack(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsConfigDeliveryChannel(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", "default")


class AwsConfigOrganizationConformancePack(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsConfigOrganizationCustomPolicyRule(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsConfigOrganizationCustomRule(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsConfigOrganizationManagedRule(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsConfigRemediationConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["config_rule_name"]):
            return None
        return self.attributes["config_rule_name"]


class AwsConfigRetentionConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        return "default"


class AwsConnectBotAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["instance_id", "lex_bot"]):
            return None

        instance_id = self.attributes["instance_id"]
        lex_bot = self.attributes["lex_bot"]
        bot_name = lex_bot.get("name")
        lex_region = lex_bot.get("lex_region", "us-east-1")

        return f"{instance_id}:{bot_name}:{lex_region}"


class AwsConnectContactFlow(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["instance_id", "contact_flow_id"]):
            return None
        return f"{self.attributes['instance_id']}:{self.attributes['contact_flow_id']}"


class AwsConnectContactFlowModule(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["instance_id", "contact_flow_module_id"]):
            return None
        return f"{self.attributes['instance_id']}:{self.attributes['contact_flow_module_id']}"


class AwsConnectHoursOfOperation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["instance_id", "hours_of_operation_id"]):
            return None
        return f"{self.attributes['instance_id']}:{self.attributes['hours_of_operation_id']}"


class AwsConnectInstance(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsConnectInstanceStorageConfig(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["instance_id", "association_id", "resource_type"]):
            return None
        return f"{self.attributes['instance_id']}:{self.attributes['association_id']}:{self.attributes['resource_type']}"


class AwsConnectLambdaFunctionAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["instance_id", "function_arn"]):
            return None
        return f"{self.attributes['instance_id']},{self.attributes['function_arn']}"


class AwsConnectPhoneNumber(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsConnectQueue(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["instance_id", "queue_id"]):
            return None
        return f"{self.attributes['instance_id']}:{self.attributes['queue_id']}"


class AwsConnectQuickConnect(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["instance_id", "quick_connect_id"]):
            return None
        return f"{self.attributes['instance_id']}:{self.attributes['quick_connect_id']}"


class AwsConnectRoutingProfile(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["instance_id", "routing_profile_id"]):
            return None
        return (
            f"{self.attributes['instance_id']}:{self.attributes['routing_profile_id']}"
        )


class AwsConnectSecurityProfile(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["instance_id", "security_profile_id"]):
            return None
        return (
            f"{self.attributes['instance_id']}:{self.attributes['security_profile_id']}"
        )


class AwsConnectUser(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["instance_id", "user_id"]):
            return None
        return f"{self.attributes['instance_id']}:{self.attributes['user_id']}"


class AwsConnectUserHierarchyGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["instance_id", "hierarchy_group_id"]):
            return None
        return (
            f"{self.attributes['instance_id']}:{self.attributes['hierarchy_group_id']}"
        )


class AwsConnectUserHierarchyStructure(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["instance_id"]):
            return None
        return self.attributes["instance_id"]


class AwsConnectVocabulary(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["instance_id", "vocabulary_id"]):
            return None
        return f"{self.attributes['instance_id']}:{self.attributes['vocabulary_id']}"


class AwsCostoptimizationhubEnrollmentStatus(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("account_id", None)


class AwsCostoptimizationhubPreferences(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsCurReportDefinition(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("report_name", None)


class AwsCustomerGateway(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsCustomerprofilesProfile(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["domain_name", "id"]):
            return None
        return f"{self.attributes['domain_name']}/{self.attributes['id']}"


class AwsDataexchangeDataSet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsDataexchangeRevision(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["data_set_id", "revision_id"]):
            return None
        return f"{self.attributes['data_set_id']}:{self.attributes['revision_id']}"


class AwsDatapipelinePipeline(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsDatapipelinePipelineDefinition(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["pipeline_id"]):
            return None
        return self.attributes["pipeline_id"]


class AwsDatazoneAssetType(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["domain_identifier", "name"]):
            return None
        return f"{self.attributes['domain_identifier']},{self.attributes['name']}"


class AwsDatazoneDomain(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsDatazoneEnvironment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["domain_identifier", "id"]):
            return None
        return f"{self.attributes['domain_identifier']},{self.attributes['id']}"


class AwsDatazoneEnvironmentBlueprintConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["domain_id", "environment_blueprint_id"]):
            return None
        return f"{self.attributes['domain_id']}/{self.attributes['environment_blueprint_id']}"


class AwsDatazoneEnvironmentProfile(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id", "domain_identifier"]):
            return None
        return f"{self.attributes['id']},{self.attributes['domain_identifier']}"


class AwsDatazoneFormType(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = ["domain_identifier", "name", "revision"]
        if not self.has_attributes(required_attrs):
            return None
        return f"{self.attributes['domain_identifier']},{self.attributes['name']},{self.attributes['revision']}"


class AwsDatazoneGlossary(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = ["domain_identifier", "id", "owning_project_identifier"]
        if not self.has_attributes(required_attrs):
            return None
        return f"{self.attributes['domain_identifier']},{self.attributes['id']},{self.attributes['owning_project_identifier']}"


class AwsDatazoneGlossaryTerm(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["domain_identifier", "id", "glossary_identifier"]):
            return None
        return f"{self.attributes['domain_identifier']},{self.attributes['id']},{self.attributes['glossary_identifier']}"


class AwsDatazoneProject(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["domain_id", "id"]):
            return None
        return f"{self.attributes['domain_id']}:{self.attributes['id']}"


class AwsDatazoneUserProfile(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(
            ["user_identifier", "domain_identifier", "user_type"]
        ):
            return None
        return f"{self.attributes['user_identifier']},{self.attributes['domain_identifier']},{self.attributes['user_type']}"


class AwsDaxCluster(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["cluster_name"]):
            return None
        return self.attributes["cluster_name"]


class AwsDaxParameterGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsDaxSubnetGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsDbClusterSnapshot(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["db_cluster_snapshot_identifier"]):
            return None
        return self.attributes["db_cluster_snapshot_identifier"]


class AwsDbEventSubscription(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsDbInstanceAutomatedBackupsReplication(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsDbInstanceRoleAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["db_instance_identifier", "role_arn"]):
            return None
        return (
            f"{self.attributes['db_instance_identifier']},{self.attributes['role_arn']}"
        )


class AwsDbOptionGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsDbParameterGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsDbProxy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsDbProxyDefaultTargetGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["db_proxy_name"]):
            return None
        return self.attributes["db_proxy_name"]


class AwsDbProxyEndpoint(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["db_proxy_name", "db_proxy_endpoint_name"]):
            return None
        return f"{self.attributes['db_proxy_name']}/{self.attributes['db_proxy_endpoint_name']}"


class AwsDbProxyTarget(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["db_proxy_name", "target_group_name", "type"]):
            return None

        if "db_instance_identifier" in self.attributes:
            resource_id = self.attributes["db_instance_identifier"]
        elif "db_cluster_identifier" in self.attributes:
            resource_id = self.attributes["db_cluster_identifier"]
        else:
            return None

        return f"{self.attributes['db_proxy_name']}/{self.attributes['target_group_name']}/{self.attributes['type']}/{resource_id}"


class AwsDbSnapshot(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["db_snapshot_identifier"]):
            return None
        return self.attributes["db_snapshot_identifier"]


class AwsDbSnapshotCopy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["target_db_snapshot_identifier"]):
            return None
        return self.attributes["target_db_snapshot_identifier"]


class AwsDbSubnetGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsDefaultNetworkAcl(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["default_network_acl_id"]):
            return None
        return self.attributes["default_network_acl_id"]


class AwsDefaultRouteTable(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["default_route_table_id"]):
            return None
        return self.attributes["default_route_table_id"]


class AwsDefaultSecurityGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsDefaultSubnet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsDefaultVpc(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsDefaultVpcDhcpOptions(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsDetectiveGraph(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("graph_arn", None)


class AwsDetectiveInvitationAccepter(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("graph_arn", None)


class AwsDetectiveMember(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["graph_arn", "account_id"]):
            return None
        return f"{self.attributes['graph_arn']}/{self.attributes['account_id']}"


class AwsDetectiveOrganizationAdminAccount(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("account_id", None)


class AwsDetectiveOrganizationConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("graph_arn", None)


class AwsDevicefarmDevicePool(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsDevicefarmInstanceProfile(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsDevicefarmNetworkProfile(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsDevicefarmProject(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsDevicefarmTestGridProject(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsDevicefarmUpload(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsDevopsguruEventSourcesConfig(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsDevopsguruResourceCollection(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["type"]):
            return None
        return self.attributes["type"]


class AwsDevopsguruServiceIntegration(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsDirectoryServiceConditionalForwarder(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["directory_id", "remote_domain_name"]):
            return None
        return (
            f"{self.attributes['directory_id']}:{self.attributes['remote_domain_name']}"
        )


class AwsDirectoryServiceDirectory(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsDirectoryServiceLogSubscription(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["directory_id"]):
            return None
        return self.attributes["directory_id"]


class AwsDirectoryServiceRadiusSettings(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("directory_id", None)


class AwsDirectoryServiceRegion(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["directory_id", "region_name"]):
            return None
        return f"{self.attributes['directory_id']},{self.attributes['region_name']}"


class AwsDirectoryServiceSharedDirectory(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsDirectoryServiceSharedDirectoryAccepter(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("shared_directory_id", None)


class AwsDirectoryServiceTrust(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["directory_id", "remote_domain_name"]):
            return None
        return (
            f"{self.attributes['directory_id']}/{self.attributes['remote_domain_name']}"
        )


class AwsDlmLifecyclePolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsDmsCertificate(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("certificate_id", None)


class AwsDmsEndpoint(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["endpoint_id"]):
            return None
        return self.attributes["endpoint_id"]


class AwsDmsEventSubscription(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsDmsReplicationConfig(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsDmsReplicationInstance(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["replication_instance_id"]):
            return None
        return self.attributes["replication_instance_id"]


class AwsDmsReplicationSubnetGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("replication_subnet_group_id", None)


class AwsDmsReplicationTask(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["replication_task_id"]):
            return None
        return self.attributes["replication_task_id"]


class AwsDmsS3Endpoint(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["endpoint_id"]):
            return None
        return self.attributes["endpoint_id"]


class AwsDocdbCluster(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("cluster_identifier", None)


class AwsDocdbClusterInstance(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["identifier"]):
            return None
        return self.attributes["identifier"]


class AwsDocdbClusterParameterGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsDocdbClusterSnapshot(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["db_cluster_snapshot_identifier"]):
            return None
        return self.attributes["db_cluster_snapshot_identifier"]


class AwsDocdbEventSubscription(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsDocdbGlobalCluster(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("global_cluster_identifier", None)


class AwsDocdbSubnetGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsDocdbelasticCluster(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsDrsReplicationConfigurationTemplate(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsDxBgpPeer(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(
            ["virtual_interface_id", "bgp_asn", "address_family"]
        ):
            return None
        return f"{self.attributes['virtual_interface_id']}/{self.attributes['bgp_asn']}/{self.attributes['address_family']}"


class AwsDxConnection(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsDxConnectionAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["connection_id", "lag_id"]):
            return None
        return f"{self.attributes['connection_id']}/{self.attributes['lag_id']}"


class AwsDxConnectionConfirmation(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("connection_id", None)


class AwsDxGateway(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsDxGatewayAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["dx_gateway_id", "associated_gateway_id"]):
            return None
        return f"{self.attributes['dx_gateway_id']}/{self.attributes['associated_gateway_id']}"


class AwsDxGatewayAssociationProposal(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None

        # Check if the import ID already contains multiple components
        if "/" in self.attributes["id"]:
            return self.attributes["id"]

        # If only proposal ID is provided, return it
        return self.attributes["id"]


class AwsDxHostedConnection(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsDxHostedPrivateVirtualInterface(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsDxHostedPrivateVirtualInterfaceAccepter(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("virtual_interface_id", None)


class AwsDxHostedPublicVirtualInterface(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsDxHostedPublicVirtualInterfaceAccepter(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("virtual_interface_id", None)


class AwsDxHostedTransitVirtualInterface(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsDxHostedTransitVirtualInterfaceAccepter(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("virtual_interface_id", None)


class AwsDxLag(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsDxMacsecKeyAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["connection_id"]):
            return None
        return self.attributes["connection_id"]


class AwsDxPrivateVirtualInterface(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsDxPublicVirtualInterface(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsDxTransitVirtualInterface(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsDynamodbContributorInsights(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["table_name"]):
            return None

        table_name = self.attributes["table_name"]
        index_name = self.attributes.get("index_name", "")

        if index_name:
            return f"name:{table_name}/index:{index_name}/{self.attributes.get('account_id', '')}"
        else:
            return f"name:{table_name}/index:/"


class AwsDynamodbGlobalTable(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsDynamodbKinesisStreamingDestination(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["table_name", "stream_arn"]):
            return None
        return f"{self.attributes['table_name']},{self.attributes['stream_arn']}"


class AwsDynamodbResourcePolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("resource_arn", None)


class AwsDynamodbTable(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsDynamodbTableExport(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsDynamodbTableItem(BaseResource):
    def _get_import_id(self) -> str | None:
        return None  # Import is not supported for this resource


class AwsDynamodbTableReplica(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["global_table_arn"]):
            return None

        # Extract table name from ARN
        table_name = self.attributes["global_table_arn"].split(":")[-1].split("/")[-1]

        # Extract region from ARN
        region = self.attributes["global_table_arn"].split(":")[3]

        return f"{table_name}:{region}"


class AwsDynamodbTag(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["resource_arn", "key"]):
            return None
        return f"{self.attributes['resource_arn']},{self.attributes['key']}"


class AwsEbsDefaultKmsKey(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("key_arn", None)


class AwsEbsEncryptionByDefault(BaseResource):
    def _get_import_id(self) -> str | None:
        return "default"


class AwsEbsFastSnapshotRestore(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["availability_zone", "snapshot_id"]):
            return None
        return (
            f"{self.attributes['availability_zone']},{self.attributes['snapshot_id']}"
        )


class AwsEbsSnapshot(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEbsSnapshotBlockPublicAccess(BaseResource):
    def _get_import_id(self) -> str | None:
        return "default"


class AwsEbsSnapshotCopy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsEbsSnapshotImport(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEbsVolume(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEc2AvailabilityZoneGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("group_name", None)


class AwsEc2CapacityBlockReservation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsEc2CapacityReservation(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEc2CarrierGateway(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEc2ClientVpnAuthorizationRule(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["client_vpn_endpoint_id", "target_network_cidr"]):
            return None

        import_id = f"{self.attributes['client_vpn_endpoint_id']},{self.attributes['target_network_cidr']}"

        if "access_group_id" in self.attributes:
            import_id += f",{self.attributes['access_group_id']}"

        return import_id


class AwsEc2ClientVpnEndpoint(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEc2ClientVpnNetworkAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["client_vpn_endpoint_id", "association_id"]):
            return None
        return f"{self.attributes['client_vpn_endpoint_id']},{self.attributes['association_id']}"


class AwsEc2ClientVpnRoute(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(
            ["client_vpn_endpoint_id", "target_vpc_subnet_id", "destination_cidr_block"]
        ):
            return None
        return f"{self.attributes['client_vpn_endpoint_id']},{self.attributes['target_vpc_subnet_id']},{self.attributes['destination_cidr_block']}"


class AwsEc2Fleet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEc2Host(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEc2ImageBlockPublicAccess(BaseResource):
    def _get_import_id(self) -> str | None:
        return None


class AwsEc2InstanceConnectEndpoint(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEc2InstanceMetadataDefaults(BaseResource):
    def _get_import_id(self) -> str | None:
        return None  # Import is not supported according to documentation


class AwsEc2InstanceState(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("instance_id", None)


class AwsEc2LocalGatewayRoute(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(
            ["local_gateway_route_table_id", "destination_cidr_block"]
        ):
            return None
        return f"{self.attributes['local_gateway_route_table_id']}_{self.attributes['destination_cidr_block']}"


class AwsEc2LocalGatewayRouteTableVpcAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsEc2ManagedPrefixList(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEc2ManagedPrefixListEntry(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["prefix_list_id", "cidr"]):
            return None
        return f"{self.attributes['prefix_list_id']},{self.attributes['cidr']}"


class AwsEc2NetworkInsightsAnalysis(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEc2NetworkInsightsPath(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEc2SerialConsoleAccess(BaseResource):
    def _get_import_id(self) -> str | None:
        return "default"


class AwsEc2SubnetCidrReservation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["subnet_id", "id"]):
            return None
        return f"{self.attributes['subnet_id']}:{self.attributes['id']}"


class AwsEc2Tag(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["resource_id", "key"]):
            return None
        return f"{self.attributes['resource_id']},{self.attributes['key']}"


class AwsEc2TrafficMirrorFilter(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEc2TrafficMirrorFilterRule(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["traffic_mirror_filter_id", "id"]):
            return None
        return f"{self.attributes['traffic_mirror_filter_id']}:{self.attributes['id']}"


class AwsEc2TrafficMirrorSession(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEc2TrafficMirrorTarget(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEc2TransitGateway(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEc2TransitGatewayConnect(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEc2TransitGatewayConnectPeer(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEc2TransitGatewayDefaultRouteTableAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(
            ["transit_gateway_id", "transit_gateway_route_table_id"]
        ):
            return None
        return f"{self.attributes['transit_gateway_id']}/{self.attributes['transit_gateway_route_table_id']}"


class AwsEc2TransitGatewayDefaultRouteTablePropagation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(
            ["transit_gateway_id", "transit_gateway_route_table_id"]
        ):
            return None
        return f"{self.attributes['transit_gateway_id']}:{self.attributes['transit_gateway_route_table_id']}"


class AwsEc2TransitGatewayMulticastDomain(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEc2TransitGatewayMulticastDomainAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = [
            "transit_gateway_multicast_domain_id",
            "transit_gateway_attachment_id",
            "subnet_id",
        ]
        if not self.has_attributes(required_attrs):
            return None

        return f"{self.attributes['transit_gateway_multicast_domain_id']}:{self.attributes['transit_gateway_attachment_id']}:{self.attributes['subnet_id']}"


class AwsEc2TransitGatewayMulticastGroupMember(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = [
            "transit_gateway_multicast_domain_id",
            "group_ip_address",
            "network_interface_id",
        ]
        if not self.has_attributes(required_attrs):
            return None
        return f"{self.attributes['transit_gateway_multicast_domain_id']}:{self.attributes['group_ip_address']}:{self.attributes['network_interface_id']}"


class AwsEc2TransitGatewayMulticastGroupSource(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = [
            "transit_gateway_multicast_domain_id",
            "group_ip_address",
            "network_interface_id",
        ]
        if not self.has_attributes(required_attrs):
            return None
        return f"{self.attributes['transit_gateway_multicast_domain_id']}:{self.attributes['group_ip_address']}:{self.attributes['network_interface_id']}"


class AwsEc2TransitGatewayPeeringAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEc2TransitGatewayPeeringAttachmentAccepter(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("transit_gateway_attachment_id", None)


class AwsAthenaDataCatalog(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsCloudfrontCachePolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsCloudfrontContinuousDeploymentPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsCloudfrontDistribution(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsCloudfrontFieldLevelEncryptionConfig(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsCloudfrontFieldLevelEncryptionProfile(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsCloudfrontFunction(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsCloudfrontKeyGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsCloudfrontKeyValueStore(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsCloudfrontMonitoringSubscription(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("distribution_id", None)


class AwsCloudfrontOriginAccessControl(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsCloudfrontOriginAccessIdentity(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsCloudfrontOriginRequestPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsCloudfrontPublicKey(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsCloudfrontRealtimeLogConfig(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsCloudfrontResponseHeadersPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsCloudfrontVpcOrigin(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsCloudhsmV2Cluster(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("cluster_id", None)


class AwsCloudhsmV2Hsm(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("hsm_id", None)


class AwsCloudsearchDomain(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsCloudsearchDomainServiceAccessPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("domain_name", None)


class AwsCodeartifactDomainPermissionsPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["domain"]):
            return None
        return self.attributes.get("resource_arn", None)


class AwsCodegurureviewerRepositoryAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsCodestarconnectionsConnection(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsCodestarconnectionsHost(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsComputeoptimizerEnrollmentStatus(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("account_id", None)


class AwsComputeoptimizerRecommendationPreferences(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["resource_type", "scope"]):
            return None

        scope = self.attributes["scope"][0]
        if not all(key in scope for key in ["name", "value"]):
            return None

        return f"{self.attributes['resource_type']},{scope['name']},{scope['value']}"


class AwsControltowerControl(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["target_identifier", "control_identifier"]):
            return None
        return f"{self.attributes['target_identifier']},{self.attributes['control_identifier']}"


class AwsControltowerLandingZone(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsCustomerprofilesDomain(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsDatasyncAgent(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsDatasyncLocationAzureBlob(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsDatasyncLocationEfs(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsDatasyncLocationFsxLustreFileSystem(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn", "fsx_filesystem_arn"]):
            return None
        return f"{self.attributes['arn']}#{self.attributes['fsx_filesystem_arn']}"


class AwsDatasyncLocationFsxOntapFileSystem(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn", "storage_virtual_machine_arn"]):
            return None
        return (
            f"{self.attributes['arn']}#{self.attributes['storage_virtual_machine_arn']}"
        )


class AwsDatasyncLocationFsxOpenzfsFileSystem(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn", "fsx_filesystem_arn"]):
            return None
        return f"{self.attributes['arn']}#{self.attributes['fsx_filesystem_arn']}"


class AwsDatasyncLocationFsxWindowsFileSystem(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn", "fsx_filesystem_arn"]):
            return None
        return f"{self.attributes['arn']}#{self.attributes['fsx_filesystem_arn']}"


class AwsDatasyncLocationHdfs(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsDatasyncLocationNfs(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsDatasyncLocationObjectStorage(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsDatasyncLocationS3(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsDatasyncLocationSmb(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsDatasyncTask(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsDevopsguruNotificationChannel(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsSsmMaintenanceWindow(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsQuicksightIngestion(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = ["aws_account_id", "data_set_id", "ingestion_id"]
        if not self.has_attributes(required_attrs):
            return None

        account_id = self.attributes.get("aws_account_id", "")
        data_set_id = self.attributes["data_set_id"]
        ingestion_id = self.attributes["ingestion_id"]

        return f"{account_id},{data_set_id},{ingestion_id}"


class AwsRdsReservedInstance(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("reservation_id", None)


class AwsInternetGatewayAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["internet_gateway_id", "vpc_id"]):
            return None
        return f"{self.attributes['internet_gateway_id']}:{self.attributes['vpc_id']}"


class AwsEmrStudioSessionMapping(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["studio_id", "identity_type", "identity_id"]):
            return None
        return f"{self.attributes['studio_id']}:{self.attributes['identity_type']}:{self.attributes['identity_id']}"


class AwsIvsPlaybackKeyPair(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsInspectorResourceGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsIotTopicRuleDestination(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsSsoadminApplicationAssignmentConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("application_arn", None)


class AwsMskScramSecretAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["cluster_arn"]):
            return None
        return self.attributes["cluster_arn"]


class AwsLocationPlaceIndex(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("index_name", None)


class AwsLightsailLbCertificate(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["lb_name", "name"]):
            return None
        return f"{self.attributes['lb_name']},{self.attributes['name']}"


class AwsLambdaFunctionUrl(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["function_name"]):
            return None

        if "qualifier" in self.attributes and self.attributes["qualifier"]:
            return f"{self.attributes['function_name']}/{self.attributes['qualifier']}"

        return self.attributes["function_name"]


class AwsLbSslNegotiationPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name", "load_balancer", "lb_port"]):
            return None
        return f"{self.attributes['load_balancer']}:{self.attributes['lb_port']}:{self.attributes['name']}"


class AwsSesReceiptRuleSet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("rule_set_name", None)


class AwsRedshiftserverlessUsageLimit(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsLexIntent(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsNetworkfirewallFirewallPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsEcrRepositoryCreationTemplate(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["prefix"]):
            return None
        return self.attributes["prefix"]


class AwsQuicksightGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = ["aws_account_id", "namespace", "group_name"]
        if not self.has_attributes(required_attrs):
            return None

        account_id = self.attributes.get("aws_account_id")
        namespace = self.attributes.get("namespace", "default")
        group_name = self.attributes.get("group_name")

        return f"{account_id}/{namespace}/{group_name}"


class AwsQldbStream(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["ledger_name", "stream_name"]):
            return None
        return f"{self.attributes['ledger_name']}/{self.attributes['stream_name']}"


class AwsStoragegatewayCachedIscsiVolume(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsServicequotasServiceQuota(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["service_code", "quota_code"]):
            return None
        return f"{self.attributes['service_code']}/{self.attributes['quota_code']}"


class AwsS3BucketAnalyticsConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["bucket", "name"]):
            return None
        return f"{self.attributes['bucket']}:{self.attributes['name']}"


class AwsWafv2RegexPatternSet(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id", "name", "scope"]):
            return None
        return f"{self.attributes['id']}/{self.attributes['name']}/{self.attributes['scope']}"


class AwsEc2TransitGatewayRouteTable(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsVpcIpamResourceDiscovery(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsServiceDiscoveryHttpNamespace(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsSecurityhubMember(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["account_id"]):
            return None
        return self.attributes["account_id"]


class AwsLoadBalancerListenerPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["load_balancer_name", "load_balancer_port"]):
            return None
        return f"{self.attributes['load_balancer_name']}:{self.attributes['load_balancer_port']}"


class AwsLightsailContainerServiceDeploymentVersion(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["service_name", "version"]):
            return None
        return f"{self.attributes['service_name']}/{self.attributes['version']}"


class AwsShieldDrtAccessRoleArnAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("account_id", None)


class AwsRedshiftAuthenticationProfile(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("authentication_profile_name", None)


class AwsRdsCustomDbEngineVersion(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["engine", "engine_version"]):
            return None
        return f"{self.attributes['engine']}:{self.attributes['engine_version']}"


class AwsSagemakerWorkteam(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["workteam_name"]):
            return None
        return self.attributes["workteam_name"]


class AwsOpsworksInstance(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsLambdaPermission(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["function_name", "statement_id"]):
            return None

        qualifier = self.attributes.get("qualifier")
        if qualifier:
            return f"{self.attributes['function_name']}:{qualifier}/{self.attributes['statement_id']}"

        return f"{self.attributes['function_name']}/{self.attributes['statement_id']}"


class AwsMacie2OrganizationAdminAccount(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsRoute53HostedZoneDnssec(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["hosted_zone_id"]):
            return None
        return self.attributes["hosted_zone_id"]


class AwsLightsailCertificate(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsPinpointEmailTemplate(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["template_name"]):
            return None
        return self.attributes["template_name"]


class AwsVpcEndpointServiceAllowedPrincipal(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["vpc_endpoint_service_id", "principal_arn"]):
            return None
        return f"{self.attributes['vpc_endpoint_service_id']}|{self.attributes['principal_arn']}"


class AwsVpnGateway(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsS3controlAccessGrant(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["account_id", "access_grant_id"]):
            return None
        return f"{self.attributes['account_id']},{self.attributes['access_grant_id']}"


class AwsFsxOntapFileSystem(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsSesv2ConfigurationSetEventDestination(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(
            ["configuration_set_name", "event_destination_name"]
        ):
            return None
        return f"{self.attributes['configuration_set_name']}|{self.attributes['event_destination_name']}"


class AwsIdentitystoreGroupMembership(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["identity_store_id", "membership_id"]):
            return None
        return (
            f"{self.attributes['identity_store_id']}/{self.attributes['membership_id']}"
        )


class AwsIamPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsStoragegatewayTapePool(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsSsoadminManagedPolicyAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = ["managed_policy_arn", "permission_set_arn", "instance_arn"]
        if not self.has_attributes(required_attrs):
            return None
        return f"{self.attributes['managed_policy_arn']},{self.attributes['permission_set_arn']},{self.attributes['instance_arn']}"


class AwsVpcEndpointPrivateDns(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["vpc_endpoint_id"]):
            return None
        return self.attributes["vpc_endpoint_id"]


class AwsNetworkmanagerVpcAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsVpcEndpointSecurityGroupAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["vpc_endpoint_id", "security_group_id"]):
            return None
        return f"{self.attributes['vpc_endpoint_id']}|{self.attributes['security_group_id']}"


class AwsRoute53ResolverQueryLogConfigAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsElasticacheReservedCacheNode(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsGuarddutyMember(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["detector_id", "account_id"]):
            return None
        return f"{self.attributes['detector_id']}:{self.attributes['account_id']}"


class AwsRoute53ResolverRuleAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsLambdaRuntimeManagementConfig(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["function_name"]):
            return None

        qualifier = self.attributes.get("qualifier", "$LATEST")
        return f"{self.attributes['function_name']},{qualifier}"


class AwsElasticBeanstalkApplication(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsLicensemanagerGrantAccepter(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("grant_arn", None)


class AwsStoragegatewayStoredIscsiVolume(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["volume_arn"]):
            return None
        return self.attributes["volume_arn"]


class AwsRedshiftserverlessResourcePolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("resource_arn", None)


class AwsRdsIntegration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsGlueRegistry(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsSagemakerMlflowTrackingServer(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["tracking_server_name"]):
            return None
        return self.attributes["tracking_server_name"]


class AwsEfsReplicationConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["source_file_system_id"]):
            return None
        return self.attributes["source_file_system_id"]


class AwsLakeformationResource(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsElasticsearchDomain(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["domain_name"]):
            return None
        return self.attributes["domain_name"]


class AwsServicecatalogPortfolioShare(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["portfolio_id", "principal_id", "type"]):
            return None
        return f"{self.attributes['portfolio_id']}:{self.attributes['type']}:{self.attributes['principal_id']}"


class AwsElb(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsOpensearchVpcEndpoint(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsRedshiftSubnetGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsWafv2RuleGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id", "name", "scope"]):
            return None
        return f"{self.attributes['id']}/{self.attributes['name']}/{self.attributes['scope']}"


class AwsSagemakerPipeline(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("pipeline_name", None)


class AwsIamServiceLinkedRole(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsFsxDataRepositoryAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsNetworkmanagerConnection(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsElasticacheUser(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["user_id"]):
            return None
        return self.attributes["user_id"]


class AwsSagemakerDeviceFleet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("device_fleet_name", None)


class AwsRdsInstanceState(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["identifier"]):
            return None
        return self.attributes["identifier"]


class AwsNetworkmonitorMonitor(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsVpcIpamPool(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsShieldProtection(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsWafSizeConstraintSet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsPinpointGcmChannel(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["application_id"]):
            return None
        return self.attributes["application_id"]


class AwsSagemakerEndpoint(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsEc2TransitGatewayRouteTablePropagation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(
            ["transit_gateway_route_table_id", "transit_gateway_attachment_id"]
        ):
            return None
        return f"{self.attributes['transit_gateway_route_table_id']}_{self.attributes['transit_gateway_attachment_id']}"


class AwsNetworkmanagerCustomerGatewayAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["global_network_id", "customer_gateway_arn"]):
            return None
        return f"{self.attributes['global_network_id']},{self.attributes['customer_gateway_arn']}"


class AwsServiceDiscoveryService(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsLoadBalancerBackendServerPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["load_balancer_name", "instance_port"]):
            return None
        return f"{self.attributes['load_balancer_name']}:{self.attributes['instance_port']}"


class AwsMediaPackagev2ChannelGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsQuicksightUser(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["aws_account_id", "namespace", "user_name"]):
            return None
        return f"{self.attributes['aws_account_id']}/{self.attributes.get('namespace', 'default')}/{self.attributes['user_name']}"


class AwsSsmPatchBaseline(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsVpcBlockPublicAccessExclusion(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsS3controlStorageLensConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["config_id"]):
            return None

        account_id = self.attributes.get("account_id", "")
        config_id = self.attributes["config_id"]

        if not account_id:
            return None

        return f"{account_id}:{config_id}"


class AwsSecuritylakeDataLake(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsLexv2modelsIntent(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = ["intent_id", "bot_id", "bot_version", "locale_id"]
        if not self.has_attributes(required_attrs):
            return None

        return f"{self.attributes['intent_id']}:{self.attributes['bot_id']}:{self.attributes['bot_version']}:{self.attributes['locale_id']}"


class AwsRedshiftSnapshotCopyGrant(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("snapshot_copy_grant_name", None)


class AwsOrganizationsAccount(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None

        # Check if iam_user_access_to_billing is set
        if self.attributes.get("iam_user_access_to_billing"):
            return f"{self.attributes['id']}_{self.attributes['iam_user_access_to_billing']}"

        return self.attributes["id"]


class AwsSfnAlias(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsRedshiftserverlessSnapshot(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("snapshot_name", None)


class AwsVpnGatewayRoutePropagation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["vpn_gateway_id", "route_table_id"]):
            return None
        return (
            f"{self.attributes['route_table_id']}/{self.attributes['vpn_gateway_id']}"
        )


class AwsKinesisAnalyticsApplication(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsSecurityhubProductSubscription(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["product_arn", "arn"]):
            return None
        return f"{self.attributes['product_arn']},{self.attributes['arn']}"


class AwsLambdaProvisionedConcurrencyConfig(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["function_name", "qualifier"]):
            return None
        return f"{self.attributes['function_name']},{self.attributes['qualifier']}"


class AwsLexv2modelsBotLocale(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["locale_id", "bot_id", "bot_version"]):
            return None
        return f"{self.attributes['locale_id']},{self.attributes['bot_id']},{self.attributes['bot_version']}"


class AwsGlobalacceleratorCrossAccountAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsOsisPipeline(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("pipeline_name", None)


class AwsEcrRegistryPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("registry_id", None)


class AwsTransferUser(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["server_id", "user_name"]):
            return None
        return f"{self.attributes['server_id']}/{self.attributes['user_name']}"


class AwsVpnConnectionRoute(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["vpn_connection_id", "destination_cidr_block"]):
            return None
        return f"{self.attributes['vpn_connection_id']}:{self.attributes['destination_cidr_block']}"


class AwsLocationRouteCalculator(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("calculator_name", None)


class AwsIotThingGroupMembership(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["thing_group_name", "thing_name"]):
            return None
        return f"{self.attributes['thing_group_name']}/{self.attributes['thing_name']}"


class AwsMemorydbCluster(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsRedshiftEndpointAccess(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("endpoint_name", None)


class AwsOrganizationsDelegatedAdministrator(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["account_id", "service_principal"]):
            return None
        return f"{self.attributes['account_id']}/{self.attributes['service_principal']}"


class AwsSesReceiptFilter(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsGlobalacceleratorEndpointGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsSsmMaintenanceWindowTarget(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["window_id", "id"]):
            return None
        return f"{self.attributes['window_id']}/{self.attributes['id']}"


class AwsRoute53recoverycontrolconfigControlPanel(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsPinpointApnsVoipChannel(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["application_id"]):
            return None
        return self.attributes["application_id"]


class AwsS3controlAccessGrantsInstanceResourcePolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("account_id") or self.attributes.get(
            "aws:caller_account"
        )


class AwsGuarddutyThreatintelset(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["detector_id", "id"]):
            return None
        return f"{self.attributes['detector_id']}:{self.attributes['id']}"


class AwsQuicksightFolder(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["aws_account_id", "folder_id"]):
            return None
        return f"{self.attributes.get('aws_account_id')},{self.attributes.get('folder_id')}"


class AwsSecretsmanagerSecretVersion(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["secret_id", "version_id"]):
            return None
        return f"{self.attributes['secret_id']}|{self.attributes['version_id']}"


class AwsRedshiftCluster(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["cluster_identifier"]):
            return None
        return self.attributes["cluster_identifier"]


class AwsIamAccountAlias(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("account_alias", None)


class AwsIamUserPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["user", "name"]):
            return None
        return f"{self.attributes['user']}:{self.attributes['name']}"


class AwsSesIdentityNotificationTopic(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["identity", "notification_type"]):
            return None
        return f"{self.attributes['identity']}|{self.attributes['notification_type']}"


class AwsFmsResourceSet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsVpcIpamResourceDiscoveryAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsRdsCluster(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["cluster_identifier"]):
            return None
        return self.attributes["cluster_identifier"]


class AwsS3tablesTablePolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["table_bucket_arn", "namespace", "name"]):
            return None
        return f"{self.attributes['table_bucket_arn']};{self.attributes['namespace']};{self.attributes['name']}"


class AwsGlueResourcePolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("aws_account_id", None)


class AwsWafregionalSizeConstraintSet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsSsoadminApplicationAccessScope(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["application_arn", "scope"]):
            return None
        return f"{self.attributes['application_arn']},{self.attributes['scope']}"


class AwsServiceDiscoveryPublicDnsNamespace(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsLakeformationLfTag(BaseResource):
    def _get_import_id(self) -> str | None:
        catalog_id = self.attributes.get("catalog_id") or self.attributes.get(
            "aws_account_id"
        )
        key = self.attributes.get("key")

        if not catalog_id or not key:
            return None

        return f"{catalog_id}:{key}"


class AwsIamServiceSpecificCredential(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(
            ["service_name", "user_name", "service_specific_credential_id"]
        ):
            return None
        return f"{self.attributes['service_name']}:{self.attributes['user_name']}:{self.attributes['service_specific_credential_id']}"


class AwsNetworkmanagerLink(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsRedshiftSnapshotScheduleAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["cluster_identifier", "schedule_identifier"]):
            return None
        return f"{self.attributes['cluster_identifier']}/{self.attributes['schedule_identifier']}"


class AwsRamResourceAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["resource_share_arn", "resource_arn"]):
            return None
        return (
            f"{self.attributes['resource_share_arn']},{self.attributes['resource_arn']}"
        )


class AwsRedshiftHsmConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["hsm_configuration_identifier"]):
            return None
        return self.attributes["hsm_configuration_identifier"]


class AwsVpclatticeServiceNetwork(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsRedshiftserverlessNamespace(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("namespace_name", None)


class AwsElasticsearchVpcEndpoint(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsNetworkmanagerDxGatewayAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsIamGroupPolicyAttachmentsExclusive(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["group_name"]):
            return None
        return self.attributes["group_name"]


class AwsElasticacheGlobalReplicationGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("global_replication_group_id", None)


class AwsGluePartition(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = [
            "catalog_id",
            "database_name",
            "table_name",
            "partition_values",
        ]
        if not self.has_attributes(required_attrs):
            return None

        catalog_id = self.attributes.get(
            "catalog_id", self.attributes.get("account_id")
        )
        database_name = self.attributes["database_name"]
        table_name = self.attributes["table_name"]
        partition_values = self.attributes["partition_values"]

        partition_values_str = "#".join(partition_values)

        return f"{catalog_id}:{database_name}:{table_name}:{partition_values_str}"


class AwsWafregionalXssMatchSet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsOpensearchInboundConnectionAccepter(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("connection_id", None)


class AwsRoute53VpcAssociationAuthorization(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["zone_id", "vpc_id"]):
            return None
        return f"{self.attributes['zone_id']}:{self.attributes['vpc_id']}"


class AwsWafRule(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsServicequotasTemplateAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsElasticacheParameterGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsElasticacheSubnetGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsRoute53ResolverFirewallConfig(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsPinpointEmailChannel(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["application_id"]):
            return None
        return self.attributes["application_id"]


class AwsImagebuilderInfrastructureConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsOpsworksCustomLayer(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsSecurityhubOrganizationAdminAccount(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("admin_account_id", None)


class AwsVpcIpv4CidrBlockAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsLightsailDisk(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsLexBotAlias(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["bot_name", "name"]):
            return None
        return f"{self.attributes['bot_name']}:{self.attributes['name']}"


class AwsSecuritylakeAwsLogSource(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["source"]):
            return None
        source_name = self.attributes["source"].get("source_name")
        return source_name if source_name else None


class AwsFmsPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsOpsworksRdsDbInstance(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["stack_id", "rds_db_instance_arn"]):
            return None
        return f"{self.attributes['stack_id']}/{self.attributes['rds_db_instance_arn']}"


class AwsRoute53profilesProfile(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsSsmServiceSetting(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("setting_id", None)


class AwsFsxFileCache(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsS3BucketMetric(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["bucket", "name"]):
            return None
        return f"{self.attributes['bucket']}:{self.attributes['name']}"


class AwsSecurityhubInsight(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsWafregionalWebAcl(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsS3BucketObjectLockConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["bucket"]):
            return None

        if self.attributes.get("expected_bucket_owner"):
            return f"{self.attributes['bucket']},{self.attributes['expected_bucket_owner']}"

        return self.attributes["bucket"]


class AwsSsmMaintenanceWindowTask(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["window_id", "window_task_id"]):
            return None
        return f"{self.attributes['window_id']}/{self.attributes['window_task_id']}"


class AwsRamPrincipalAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["resource_share_arn", "principal"]):
            return None
        return f"{self.attributes['resource_share_arn']},{self.attributes['principal']}"


class AwsTranscribeLanguageModel(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["model_name"]):
            return None
        return self.attributes["model_name"]


class AwsQuicksightGroupMembership(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = ["aws_account_id", "namespace", "group_name", "member_name"]
        if not self.has_attributes(required_attrs):
            return None

        account_id = self.attributes.get("aws_account_id", "")
        namespace = self.attributes.get("namespace", "default")
        group_name = self.attributes["group_name"]
        member_name = self.attributes["member_name"]

        return f"{account_id}/{namespace}/{group_name}/{member_name}"


class AwsEipAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsGameliftAlias(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsS3controlBucket(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsNeptuneClusterEndpoint(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(
            ["cluster_identifier", "cluster_endpoint_identifier"]
        ):
            return None
        return f"{self.attributes['cluster_identifier']}:{self.attributes['cluster_endpoint_identifier']}"


class AwsGlueDevEndpoint(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsIamRolePolicyAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["role", "policy_arn"]):
            return None
        return f"{self.attributes['role']}/{self.attributes['policy_arn']}"


class AwsEfsMountTarget(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsLexSlotType(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsQuicksightRefreshSchedule(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = ["aws_account_id", "data_set_id", "schedule_id"]
        if not self.has_attributes(required_attrs):
            return None

        account_id = self.attributes.get("aws_account_id", "")
        data_set_id = self.attributes["data_set_id"]
        schedule_id = self.attributes["schedule_id"]

        return f"{account_id},{data_set_id},{schedule_id}"


class AwsFsxOntapVolume(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsKinesisFirehoseDeliveryStream(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsNetworkmanagerTransitGatewayRouteTableAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsKmsKey(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsSqsQueueRedrivePolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("queue_url", None)


class AwsIamSigningCertificate(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["certificate_id", "user_name"]):
            return None
        return f"{self.attributes['certificate_id']}:{self.attributes['user_name']}"


class AwsVpcDhcpOptionsAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("vpc_id", None)


class AwsNetworkmanagerTransitGatewayConnectPeerAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(
            ["global_network_id", "transit_gateway_connect_peer_arn"]
        ):
            return None
        return f"{self.attributes['global_network_id']},{self.attributes['transit_gateway_connect_peer_arn']}"


class AwsRoute53KeySigningKey(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["hosted_zone_id", "key_management_service_arn"]):
            return None
        return f"{self.attributes['hosted_zone_id']},{self.attributes['key_management_service_arn']}"


class AwsVerifiedpermissionsIdentitySource(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["policy_store_id", "id"]):
            return None
        return f"{self.attributes['policy_store_id']}:{self.attributes['id']}"


class AwsRedshiftHsmClientCertificate(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("hsm_client_certificate_identifier", None)


class AwsElasticBeanstalkConfigurationTemplate(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name", "application"]):
            return None
        return f"{self.attributes['application']}/{self.attributes['name']}"


class AwsQuicksightVpcConnection(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["aws_account_id", "vpc_connection_id"]):
            return None
        return f"{self.attributes['aws_account_id']},{self.attributes['vpc_connection_id']}"


class AwsSagemakerStudioLifecycleConfig(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("studio_lifecycle_config_name", None)


class AwsSagemakerModel(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsImagebuilderImageRecipe(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsServicecatalogappregistryApplication(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsSsoadminTrustedTokenIssuer(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsMedialiveMultiplexProgram(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["program_name", "multiplex_id"]):
            return None
        return f"{self.attributes['program_name']}/{self.attributes['multiplex_id']}"


class AwsServiceDiscoveryPrivateDnsNamespace(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id", "vpc"]):
            return None
        return f"{self.attributes['id']}:vpc-{self.attributes['vpc']}"


class AwsPinpointsmsvoicev2PhoneNumber(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsOrganizationsResourcePolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsRolesanywhereProfile(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsQuicksightFolderMembership(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = ["aws_account_id", "folder_id", "member_type", "member_id"]
        if not self.has_attributes(required_attrs):
            return None

        account_id = self.attributes.get("aws_account_id", "")
        folder_id = self.attributes["folder_id"]
        member_type = self.attributes["member_type"]
        member_id = self.attributes["member_id"]

        return f"{account_id},{folder_id},{member_type},{member_id}"


class AwsVpcEndpointConnectionAccepter(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["vpc_endpoint_service_id", "vpc_endpoint_id"]):
            return None
        return f"{self.attributes['vpc_endpoint_service_id']}_{self.attributes['vpc_endpoint_id']}"


class AwsIotPolicyAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["policy", "target"]):
            return None
        return f"{self.attributes['policy']}|{self.attributes['target']}"


class AwsSfnStateMachine(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsIvschatRoom(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsLightsailDatabase(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["relational_database_name"]):
            return None
        return self.attributes["relational_database_name"]


class AwsRekognitionCollection(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("collection_id", None)


class AwsTimestreamwriteTable(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["table_name", "database_name"]):
            return None
        return f"{self.attributes['table_name']}:{self.attributes['database_name']}"


class AwsKeyspacesKeyspace(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsGameliftGameSessionQueue(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsLexv2modelsSlot(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = ["bot_id", "bot_version", "intent_id", "locale_id", "slot_id"]
        if not self.has_attributes(required_attrs):
            return None
        return f"{self.attributes['bot_id']},{self.attributes['bot_version']},{self.attributes['intent_id']},{self.attributes['locale_id']},{self.attributes['slot_id']}"


class AwsServicecatalogTagOption(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsPinpointSmsChannel(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("application_id", None)


class AwsEcrAccountSetting(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsSesv2EmailIdentityMailFromAttributes(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["email_identity"]):
            return None
        return self.attributes["email_identity"]


class AwsWorkspacesIpGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsIamAccessKey(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["user"]):
            return None
        return self.attributes.get("id", None)


class AwsRedshiftDataShareConsumerAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["data_share_arn"]):
            return None

        associate_entire_account = self.attributes.get("associate_entire_account", "")
        consumer_arn = self.attributes.get("consumer_arn", "")
        consumer_region = self.attributes.get("consumer_region", "")

        return f"{self.attributes['data_share_arn']},{associate_entire_account},{consumer_arn},{consumer_region}"


class AwsFinspaceKxDatabase(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["environment_id", "name"]):
            return None
        return f"{self.attributes['environment_id']},{self.attributes['name']}"


class AwsEmrcontainersVirtualCluster(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsSignerSigningProfile(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsNetworkAclRule(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = ["network_acl_id", "rule_number", "protocol", "egress"]
        if not self.has_attributes(required_attrs):
            return None

        network_acl_id = self.attributes["network_acl_id"]
        rule_number = self.attributes["rule_number"]
        protocol = self.attributes["protocol"]
        egress = str(self.attributes["egress"]).lower()

        return f"{network_acl_id}:{rule_number}:{protocol}:{egress}"


class AwsTransferTag(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["resource_arn", "key"]):
            return None
        return f"{self.attributes['resource_arn']},{self.attributes['key']}"


class AwsOrganizationsPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsSesDomainIdentity(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("domain", None)


class AwsVpcPeeringConnection(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsRumMetricsDestination(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("app_monitor_name", None)


class AwsSesv2AccountVdmAttributes(BaseResource):
    def _get_import_id(self) -> str | None:
        return "ses-account-vdm-attributes"


class AwsInspectorAssessmentTemplate(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsIamUserLoginProfile(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["user"]):
            return None
        return self.attributes["user"]


class AwsOpsworksApplication(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsResourcegroupsResource(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["group_arn", "resource_arn"]):
            return None
        return f"{self.attributes['group_arn']},{self.attributes['resource_arn']}"


class AwsLightsailDistribution(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes.get("name", None)


class AwsSnsPlatformApplication(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsS3BucketInventory(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["bucket", "name"]):
            return None
        return f"{self.attributes['bucket']}:{self.attributes['name']}"


class AwsRoute53domainsRegisteredDomain(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["domain_name"]):
            return None
        return self.attributes["domain_name"]


class AwsLightsailBucketResourceAccess(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["bucket_name", "resource_name"]):
            return None
        return f"{self.attributes['bucket_name']},{self.attributes['resource_name']}"


class AwsS3BucketPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("bucket", None)


class AwsSsmcontactsRotation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsLexv2modelsSlotType(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = ["bot_id", "bot_version", "locale_id", "slot_type_id"]
        if not self.has_attributes(required_attrs):
            return None
        return f"{self.attributes['bot_id']},{self.attributes['bot_version']},{self.attributes['locale_id']},{self.attributes['slot_type_id']}"


class AwsMemorydbMultiRegionCluster(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("multi_region_cluster_name", None)


class AwsLbListenerRule(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsSchedulerScheduleGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsSyntheticsCanary(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsRedshiftScheduledAction(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsGuarddutyOrganizationConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("detector_id", None)


class AwsStoragegatewayWorkingStorage(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["gateway_arn", "disk_id"]):
            return None
        return f"{self.attributes['gateway_arn']}:{self.attributes['disk_id']}"


class AwsIdentitystoreUser(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["identity_store_id", "user_id"]):
            return None
        return f"{self.attributes['identity_store_id']}/{self.attributes['user_id']}"


class AwsEcrLifecyclePolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["repository"]):
            return None
        return self.attributes["repository"]


class AwsS3controlBucketLifecycleConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["bucket"]):
            return None
        return self.attributes["bucket"]


class AwsFinspaceKxCluster(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["environment_id", "name"]):
            return None
        return f"{self.attributes['environment_id']},{self.attributes['name']}"


class AwsOpensearchDomainPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["domain_name"]):
            return None
        return self.attributes["domain_name"]


class AwsLightsailDiskAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["disk_name", "instance_name"]):
            return None
        return f"{self.attributes['disk_name']},{self.attributes['instance_name']}"


class AwsRouteTable(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsGameliftBuild(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsS3BucketCorsConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["bucket"]):
            return None

        if self.attributes.get("expected_bucket_owner"):
            return f"{self.attributes['bucket']},{self.attributes['expected_bucket_owner']}"

        return self.attributes["bucket"]


class AwsIamUserPolicyAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["user", "policy_arn"]):
            return None
        return f"{self.attributes['user']}/{self.attributes['policy_arn']}"


class AwsFsxOpenzfsSnapshot(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsTimestreaminfluxdbDbInstance(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsEcsTag(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["resource_arn", "key"]):
            return None
        return f"{self.attributes['resource_arn']},{self.attributes['key']}"


class AwsKendraDataSource(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["index_id", "data_source_id"]):
            return None
        return f"{self.attributes['data_source_id']}/{self.attributes['index_id']}"


class AwsSchemasRegistry(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsTransferConnector(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("connector_id", None)


class AwsEksAccessEntry(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["cluster_name", "principal_arn"]):
            return None
        return f"{self.attributes['cluster_name']}:{self.attributes['principal_arn']}"


class AwsIamInstanceProfile(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsLambdaLayerVersion(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsSqsQueuePolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("queue_url", None)


class AwsRolesanywhereTrustAnchor(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsQuicksightDataSource(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["data_source_id"]):
            return None

        account_id = self.attributes.get("aws_account_id", "")
        data_source_id = self.attributes["data_source_id"]

        return f"{account_id}/{data_source_id}" if account_id else data_source_id


class AwsGuarddutyDetectorFeature(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["detector_id", "name"]):
            return None
        return f"{self.attributes['detector_id']}/{self.attributes['name']}"


class AwsSagemakerAppImageConfig(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["app_image_config_name"]):
            return None
        return self.attributes["app_image_config_name"]


class AwsIamAccountPasswordPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return "iam-account-password-policy"


class AwsXraySamplingRule(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("rule_name", None)


class AwsVpcIpamOrganizationAdminAccount(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("delegated_admin_account_id", None)


class AwsServicecatalogPrincipalPortfolioAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = [
            "accept_language",
            "principal_arn",
            "portfolio_id",
            "principal_type",
        ]
        if not self.has_attributes(required_attrs):
            return None

        return f"{self.attributes['accept_language']},{self.attributes['principal_arn']},{self.attributes['portfolio_id']},{self.attributes['principal_type']}"


class AwsRoute53ResolverFirewallRule(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(
            ["firewall_rule_group_id", "firewall_domain_list_id"]
        ):
            return None
        return f"{self.attributes['firewall_rule_group_id']}:{self.attributes['firewall_domain_list_id']}"


class AwsIvsChannel(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsPinpointBaiduChannel(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["application_id"]):
            return None
        return self.attributes["application_id"]


class AwsSecurityhubFindingAggregator(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsS3BucketLifecycleConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["bucket"]):
            return None

        if "expected_bucket_owner" in self.attributes:
            return f"{self.attributes['bucket']},{self.attributes['expected_bucket_owner']}"

        return self.attributes["bucket"]


class AwsRoute53ResolverConfig(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsVerifiedpermissionsPolicyTemplate(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["policy_store_id", "policy_template_id"]):
            return None
        return f"{self.attributes['policy_store_id']}:{self.attributes['policy_template_id']}"


class AwsShieldProtectionHealthCheckAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["shield_protection_id", "health_check_arn"]):
            return None
        return f"{self.attributes['shield_protection_id']}+{self.attributes['health_check_arn']}"


class AwsVpclatticeResourceGateway(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsSecurityhubConfigurationPolicyAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["target_id"]):
            return None
        return self.attributes["target_id"]


class AwsLightsailKeyPair(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsVpclatticeServiceNetworkVpcAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsSecurityhubActionTarget(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsPrometheusRuleGroupNamespace(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsEcrRepositoryPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["repository"]):
            return None
        return self.attributes["repository"]


class AwsQuicksightAccountSubscription(BaseResource):
    def _get_import_id(self) -> str | None:
        return None


class AwsStoragegatewaySmbFileShare(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsVpcPeeringConnectionOptions(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["vpc_peering_connection_id"]):
            return None
        return self.attributes["vpc_peering_connection_id"]


class AwsGuarddutyMalwareProtectionPlan(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsOpsworksJavaAppLayer(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsSagemakerImage(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("image_name", None)


class AwsShieldDrtAccessLogBucketAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("log_bucket", None)


class AwsGlobalacceleratorCustomRoutingListener(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsS3controlObjectLambdaAccessPoint(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name", "account_id"]):
            return None
        account_id = self.attributes.get("account_id", "")
        name = self.attributes.get("name", "")
        return f"{account_id}:{name}"


class AwsSesDomainIdentityVerification(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("domain", None)


class AwsFsxBackup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsVpnGatewayAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["vpc_id", "vpn_gateway_id"]):
            return None
        return f"{self.attributes['vpn_gateway_id']}/{self.attributes['vpc_id']}"


class AwsRdsExportTask(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["export_task_identifier"]):
            return None
        return self.attributes["export_task_identifier"]


class AwsLightsailLbAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["lb_name", "instance_name"]):
            return None
        return f"{self.attributes['lb_name']},{self.attributes['instance_name']}"


class AwsRoute53recoverycontrolconfigCluster(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsElasticacheServerlessCache(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsVolumeAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["device_name", "volume_id", "instance_id"]):
            return None
        return f"{self.attributes['device_name']}:{self.attributes['volume_id']}:{self.attributes['instance_id']}"


class AwsElastictranscoderPreset(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsRdsClusterEndpoint(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["cluster_endpoint_identifier"]):
            return None
        return self.attributes["cluster_endpoint_identifier"]


class AwsRoute53recoveryreadinessResourceSet(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["resource_set_name"]):
            return None
        return self.attributes["resource_set_name"]


class AwsWafregionalIpset(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsOpsworksUserProfile(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("user_arn", None)


class AwsLightsailDomain(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("domain_name", None)


class AwsGameliftScript(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsWafWebAcl(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEcrRegistryScanningConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("registry_id", None)


class AwsVpcIpamPreviewNextCidr(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsSesTemplate(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsEksIdentityProviderConfig(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["cluster_name", "oidc"]):
            return None

        cluster_name = self.attributes["cluster_name"]
        config_name = self.attributes["oidc"].get("identity_provider_config_name")

        if not cluster_name or not config_name:
            return None

        return f"{cluster_name}:{config_name}"


class AwsElasticBeanstalkEnvironment(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsFinspaceKxUser(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["environment_id", "name"]):
            return None
        return f"{self.attributes['environment_id']},{self.attributes['name']}"


class AwsRoute53DelegationSet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsSsmParameter(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsEcrPullThroughCacheRule(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["ecr_repository_prefix"]):
            return None
        return self.attributes["ecr_repository_prefix"]


class AwsEmrserverlessApplication(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsNetworkmanagerCoreNetwork(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsRoute53domainsDelegationSignerRecord(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["domain_name", "dnssec_key_id"]):
            return None
        return f"{self.attributes['domain_name']},{self.attributes['dnssec_key_id']}"


class AwsVerifiedaccessTrustProvider(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsLicensemanagerLicenseConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsLambdaEventSourceMapping(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("uuid", None)


class AwsWafregionalSqlInjectionMatchSet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsTransferWorkflow(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsSagemakerUserProfile(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["domain_id", "user_profile_name"]):
            return None
        return f"arn:aws:sagemaker:{self.attributes.get('region', 'us-west-2')}:{self.attributes.get('account_id', '')}/user-profile/{self.attributes['domain_id']}/{self.attributes['user_profile_name']}"


class AwsNetworkInterface(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsVpclatticeTargetGroupAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["target_group_identifier", "target"]):
            return None
        target_id = self.attributes["target"].get("id")
        target_group_id = self.attributes["target_group_identifier"]
        return f"{target_group_id}/{target_id}"


class AwsKmsReplicaKey(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("key_id", None)


class AwsServicecatalogappregistryAttributeGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsQuicksightNamespace(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["aws_account_id", "namespace"]):
            return None
        return f"{self.attributes['aws_account_id']},{self.attributes['namespace']}"


class AwsShieldApplicationLayerAutomaticResponse(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["resource_arn"]):
            return None
        return self.attributes["resource_arn"]


class AwsLoadBalancerPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["load_balancer_name", "policy_name"]):
            return None
        return (
            f"{self.attributes['load_balancer_name']}:{self.attributes['policy_name']}"
        )


class AwsM2Deployment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["application_id", "id"]):
            return None
        return f"{self.attributes['application_id']},{self.attributes['id']}"


class AwsNeptuneClusterSnapshot(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["db_cluster_snapshot_identifier"]):
            return None
        return self.attributes["db_cluster_snapshot_identifier"]


class AwsNeptuneEventSubscription(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsRedshiftUsageLimit(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsVpclatticeServiceNetworkServiceAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsS3BucketReplicationConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["bucket"]):
            return None
        return self.attributes["bucket"]


class AwsGuarddutyInviteAccepter(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("detector_id", None)


class AwsRoute53ZoneAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["zone_id", "vpc_id"]):
            return None

        vpc_region = self.attributes.get("vpc_region")

        if vpc_region:
            return (
                f"{self.attributes['zone_id']}:{self.attributes['vpc_id']}:{vpc_region}"
            )

        return f"{self.attributes['zone_id']}:{self.attributes['vpc_id']}"


class AwsInternetmonitorMonitor(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("monitor_name", None)


class AwsIotBillingGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsMainRouteTableAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsRoute53recoverycontrolconfigRoutingControl(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsFinspaceKxEnvironment(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsIotRoleAlias(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("alias", None)


class AwsOrganizationsPolicyAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["target_id", "policy_id"]):
            return None
        return f"{self.attributes['target_id']}:{self.attributes['policy_id']}"


class AwsSesv2DedicatedIpPool(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("pool_name", None)


class AwsRdsGlobalCluster(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["global_cluster_identifier"]):
            return None
        return self.attributes["global_cluster_identifier"]


class AwsIotProvisioningTemplate(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsSecurityhubInviteAccepter(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("master_id", None)


class AwsRedshiftParameterGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsOrganizationsOrganizationalUnit(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsSimpledbDomain(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsLbTargetGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsIamSamlProvider(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsMediaPackageChannel(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("channel_id", None)


class AwsIamGroupMembership(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name", "group"]):
            return None
        return self.attributes["name"]


class AwsLakeformationDataCellsFilter(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = [
            "table_data.database_name",
            "table_data.name",
            "table_data.table_catalog_id",
            "table_data.table_name",
        ]

        if not all(
            attr.replace("table_data.", "") in self.attributes.get("table_data", {})
            for attr in required_attrs
        ):
            return None

        table_data = self.attributes.get("table_data", {})
        return f"{table_data['database_name']},{table_data['name']},{table_data['table_catalog_id']},{table_data['table_name']}"


class AwsIamVirtualMfaDevice(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsS3controlMultiRegionAccessPointPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["details"]):
            return None

        account_id = self.attributes.get(
            "account_id",
            self.attributes.get("aws_caller_identity", {})
            .get("current", {})
            .get("account_id"),
        )
        name = self.attributes.get("details", {}).get("name")

        if not account_id or not name:
            return None

        return f"{account_id}:{name}"


class AwsSesv2EmailIdentityFeedbackAttributes(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("email_identity", None)


class AwsGuarddutyFilter(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["detector_id", "name"]):
            return None
        return f"{self.attributes['detector_id']}:{self.attributes['name']}"


class AwsEmrManagedScalingPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("cluster_id", None)


class AwsEksAccessPolicyAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["cluster_name", "principal_arn", "policy_arn"]):
            return None
        return f"{self.attributes['cluster_name']}#{self.attributes['principal_arn']}#{self.attributes['policy_arn']}"


class AwsGlobalacceleratorCustomRoutingAccelerator(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsKmsReplicaExternalKey(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("key_id", None)


class AwsElasticsearchDomainSamlOptions(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["domain_name"]):
            return None
        return self.attributes["domain_name"]


class AwsTranscribeVocabularyFilter(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["vocabulary_filter_name"]):
            return None
        return self.attributes["vocabulary_filter_name"]


class AwsS3tablesTableBucketPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["table_bucket_arn"]):
            return None
        return self.attributes["table_bucket_arn"]


class AwsServicecatalogServiceAction(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsS3controlBucketPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsS3AccessPoint(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name", "account_id"]):
            return None

        # Check if this is an Outposts bucket
        if "arn" in self.attributes and "outpost" in self.attributes["arn"]:
            return self.attributes.get("arn")

        # Standard S3 bucket access point
        return f"{self.attributes['account_id']}:{self.attributes['name']}"


class AwsWafXssMatchSet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsPinpointApnsSandboxChannel(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["application_id"]):
            return None
        return self.attributes["application_id"]


class AwsWorkspacesWorkspace(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsSsmActivation(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEcsClusterCapacityProviders(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("cluster_name", None)


class AwsEipDomainName(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["allocation_id"]):
            return None
        return self.attributes["allocation_id"]


class AwsEcsTaskSet(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = ["task_set_id", "service", "cluster"]
        if not self.has_attributes(required_attrs):
            return None
        return f"{self.attributes['task_set_id']},{self.attributes['service']},{self.attributes['cluster']}"


class AwsWafRateBasedRule(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsRoute53HealthCheck(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsLocationTracker(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("tracker_name", None)


class AwsLaunchConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsGlueCatalogTableOptimizer(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = ["catalog_id", "database_name", "table_name", "type"]
        if not self.has_attributes(required_attrs):
            return None
        return f"{self.attributes['catalog_id']},{self.attributes['database_name']},{self.attributes['table_name']},{self.attributes['type']}"


class AwsRoute53ResolverFirewallRuleGroupAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsSesv2EmailIdentityPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["email_identity", "policy_name"]):
            return None
        return f"{self.attributes['email_identity']}|{self.attributes['policy_name']}"


class AwsOpensearchserverlessLifecyclePolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name", "type"]):
            return None
        return f"{self.attributes['name']}/{self.attributes['type']}"


class AwsEvidentlyFeature(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name", "project"]):
            return None
        return f"{self.attributes['name']}:{self.attributes['project']}"


class AwsFinspaceKxVolume(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["environment_id", "name"]):
            return None
        return f"{self.attributes['environment_id']},{self.attributes['name']}"


class AwsSecurityGroupRule(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = [
            "security_group_id",
            "type",
            "protocol",
            "from_port",
            "to_port",
        ]
        if not self.has_attributes(required_attrs):
            return None

        # Determine source/destination
        sources = []
        if "cidr_blocks" in self.attributes and self.attributes["cidr_blocks"]:
            sources.extend(self.attributes["cidr_blocks"])
        if (
            "ipv6_cidr_blocks" in self.attributes
            and self.attributes["ipv6_cidr_blocks"]
        ):
            sources.extend(self.attributes["ipv6_cidr_blocks"])
        if "prefix_list_ids" in self.attributes and self.attributes["prefix_list_ids"]:
            sources.extend(self.attributes["prefix_list_ids"])
        if (
            "source_security_group_id" in self.attributes
            and self.attributes["source_security_group_id"]
        ):
            sources.append(self.attributes["source_security_group_id"])
        if "self" in self.attributes and self.attributes["self"]:
            sources.append("self")

        if not sources:
            return None

        # Construct import ID
        import_id_parts = [
            self.attributes["security_group_id"],
            self.attributes["type"],
            self.attributes["protocol"]
            if self.attributes["protocol"] != "-1"
            else "all",
            str(self.attributes["from_port"]),
            str(self.attributes["to_port"]),
        ]
        import_id_parts.extend(sources)

        return "_".join(import_id_parts)


class AwsMskConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsMskconnectWorkerConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsVpclatticeAuthPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEmrCluster(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsElasticacheCluster(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["cluster_id"]):
            return None
        return self.attributes["cluster_id"]


class AwsS3BucketServerSideEncryptionConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["bucket"]):
            return None

        if "expected_bucket_owner" in self.attributes:
            return f"{self.attributes['bucket']},{self.attributes['expected_bucket_owner']}"

        return self.attributes["bucket"]


class AwsPrometheusAlertManagerDefinition(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("workspace_id", None)


class AwsOpensearchPackageAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["package_id", "domain_name"]):
            return None
        return f"{self.attributes['package_id']},{self.attributes['domain_name']}"


class AwsWafv2IpSet(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id", "name", "scope"]):
            return None
        return f"{self.attributes['id']}/{self.attributes['name']}/{self.attributes['scope']}"


class AwsRoute53TrafficPolicyInstance(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsGlobalacceleratorCustomRoutingEndpointGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsElasticacheUserGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("user_group_id", None)


class AwsOpensearchserverlessSecurityConfig(BaseResource):
    pass


class AwsWafregionalRegexMatchSet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsLakeformationResourceLfTags(BaseResource):
    def _get_import_id(self) -> str | None:
        catalog_id = self.attributes.get("catalog_id", "")

        if "database" in self.attributes:
            database_name = self.attributes["database"].get("name")
            lf_tags = self.attributes.get("lf_tag", [])

            if database_name and lf_tags:
                tag_parts = [f"{tag['key']}={tag['value']}" for tag in lf_tags]
                return f"{catalog_id or ''}:{database_name}:{','.join(tag_parts)}"

        if "table" in self.attributes:
            table = self.attributes["table"]
            database_name = table.get("database_name")
            table_name = table.get("name")
            lf_tags = self.attributes.get("lf_tag", [])

            if database_name and table_name and lf_tags:
                tag_parts = [f"{tag['key']}={tag['value']}" for tag in lf_tags]
                return f"{catalog_id or ''}:{database_name}:{table_name}:{','.join(tag_parts)}"

        if "table_with_columns" in self.attributes:
            table_with_columns = self.attributes["table_with_columns"]
            database_name = table_with_columns.get("database_name")
            table_name = table_with_columns.get("name")
            lf_tags = self.attributes.get("lf_tag", [])

            if database_name and table_name and lf_tags:
                tag_parts = [f"{tag['key']}={tag['value']}" for tag in lf_tags]
                return f"{catalog_id or ''}:{database_name}:{table_name}:{','.join(tag_parts)}"

        return None


class AwsPinpointApnsVoipSandboxChannel(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["application_id"]):
            return None
        return self.attributes["application_id"]


class AwsKinesisStream(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsVerifiedaccessEndpoint(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsRdsClusterRoleAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["db_cluster_identifier", "role_arn"]):
            return None
        return (
            f"{self.attributes['db_cluster_identifier']},{self.attributes['role_arn']}"
        )


class AwsKinesisResourcePolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("resource_arn", None)


class AwsS3outpostsEndpoint(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn", "security_group_id", "subnet_id"]):
            return None
        return f"{self.attributes['arn']},{self.attributes['security_group_id']},{self.attributes['subnet_id']}"


class AwsMemorydbSnapshot(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsIamPolicyAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsMskSingleScramSecretAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["cluster_arn", "secret_arn"]):
            return None
        return f"{self.attributes['cluster_arn']},{self.attributes['secret_arn']}"


class AwsSnsTopicPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsIotCertificate(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsKeyspacesTable(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["keyspace_name", "table_name"]):
            return None
        return f"{self.attributes['keyspace_name']}/{self.attributes['table_name']}"


class AwsRoute53recoveryreadinessRecoveryGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("recovery_group_name", None)


class AwsRedshiftdataStatement(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsInstance(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsSecurityhubAccount(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsNetworkfirewallRuleGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsPipesPipe(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsLbTargetGroupAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["target_group_arn", "target_id"]):
            return None
        return f"{self.attributes['target_group_arn']}/{self.attributes['target_id']}"


class AwsOamLink(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsSecurityhubAutomationRule(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsElbAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["elb", "instance"]):
            return None
        return f"{self.attributes['elb']}/{self.attributes['instance']}"


class AwsS3DirectoryBucket(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["bucket"]):
            return None
        return self.attributes["bucket"]


class AwsGlueSchema(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsEcsService(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["cluster", "name"]):
            return None
        return f"{self.attributes['cluster'].split('/')[-1]}/{self.attributes['name']}"


class AwsIamUserPoliciesExclusive(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["user_name"]):
            return None
        return self.attributes["user_name"]


class AwsSqsQueueRedriveAllowPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("queue_url", None)


class AwsSsoadminPermissionSetInlinePolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["permission_set_arn", "instance_arn"]):
            return None
        return (
            f"{self.attributes['permission_set_arn']},{self.attributes['instance_arn']}"
        )


class AwsSsoadminCustomerManagedPolicyAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = [
            "customer_managed_policy_reference.0.name",
            "customer_managed_policy_reference.0.path",
            "permission_set_arn",
            "instance_arn",
        ]

        if not self.has_attributes(required_attrs):
            return None

        name = self.attributes.get("customer_managed_policy_reference.0.name")
        path = self.attributes.get("customer_managed_policy_reference.0.path", "/")
        permission_set_arn = self.attributes.get("permission_set_arn")
        instance_arn = self.attributes.get("instance_arn")

        return f"{name},{path},{permission_set_arn},{instance_arn}"


class AwsGlobalacceleratorAccelerator(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsVpcEndpointPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsRdsClusterActivityStream(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("resource_arn", None)


class AwsGuarddutyOrganizationAdminAccount(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("admin_account_id", None)


class AwsRoute53Record(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["zone_id", "name", "type"]):
            return None

        zone_id = self.attributes["zone_id"]
        name = self.attributes.get("name", "")
        record_type = self.attributes["type"]

        set_identifier = self.attributes.get("set_identifier", "")

        if set_identifier:
            return f"{zone_id}_{name}_{record_type}_{set_identifier}"
        else:
            return f"{zone_id}_{name}_{record_type}"


class AwsKmsGrant(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["key_id", "grant_id"]):
            return None
        return f"{self.attributes['key_id']}:{self.attributes['grant_id']}"


class AwsSesActiveReceiptRuleSet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("rule_set_name", None)


class AwsOpensearchOutboundConnection(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsImagebuilderLifecyclePolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsMemorydbAcl(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsEc2TransitGatewayVpcAttachmentAccepter(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("transit_gateway_attachment_id", None)


class AwsInspector2Enabler(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["account_ids", "resource_types"]):
            return None
        return ",".join(sorted(self.attributes["account_ids"]))


class AwsElastictranscoderPipeline(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsShieldProtectionGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["protection_group_id"]):
            return None
        return self.attributes["protection_group_id"]


class AwsRedshiftClusterSnapshot(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["snapshot_identifier"]):
            return None
        return self.attributes["snapshot_identifier"]


class AwsMacie2InvitationAccepter(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["administrator_account_id"]):
            return None
        return self.attributes["administrator_account_id"]


class AwsEvidentlySegment(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsOpsworksPhpAppLayer(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEmrSecurityConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsVpcEndpointSubnetAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["vpc_endpoint_id", "subnet_id"]):
            return None
        return f"{self.attributes['vpc_endpoint_id']}/{self.attributes['subnet_id']}"


class AwsLightsailLbStickinessPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("lb_name", None)


class AwsSsmcontactsContactChannel(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsInspector2OrganizationConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        return ""


class AwsMskCluster(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsWorkspacesConnectionAlias(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsKmsCiphertext(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["ciphertext_blob"]):
            return None
        return self.attributes["ciphertext_blob"]


class AwsResiliencehubResiliencyPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsNetworkInterfaceSgAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["network_interface_id", "security_group_id"]):
            return None
        return f"{self.attributes['network_interface_id']}_{self.attributes['security_group_id']}"


class AwsGlueConnection(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name", "catalog_id"]):
            return None
        catalog_id = self.attributes.get(
            "catalog_id", self.attributes.get("account_id")
        )
        return f"{catalog_id}:{self.attributes['name']}"


class AwsSesEmailIdentity(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("email", None)


class AwsLightsailStaticIp(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsGrafanaWorkspaceApiKey(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["workspace_id", "key_name"]):
            return None
        return f"{self.attributes['workspace_id']}/{self.attributes['key_name']}"


class AwsWafv2WebAclAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["web_acl_arn", "resource_arn"]):
            return None
        return f"{self.attributes['web_acl_arn']},{self.attributes['resource_arn']}"


class AwsS3Object(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["bucket", "key"]):
            return None
        return f"{self.attributes['bucket']}/{self.attributes['key']}"


class AwsResourceexplorer2View(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsVerifiedaccessInstance(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsSagemakerMonitoringSchedule(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsSagemakerHub(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("hub_name", None)


class AwsSsoadminInstanceAccessControlAttributes(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["instance_arn"]):
            return None
        return self.attributes["instance_arn"]


class AwsKeyPair(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("key_name", None)


class AwsOamSinkPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("sink_identifier", None)


class AwsS3AccountPublicAccessBlock(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("account_id") or self.attributes.get("id")


class AwsEksPodIdentityAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["cluster_name", "association_id"]):
            return None
        return f"{self.attributes['cluster_name']},{self.attributes['association_id']}"


class AwsMskClusterPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("cluster_arn", None)


class AwsKendraFaq(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["faq_id", "index_id"]):
            return None
        return f"{self.attributes['faq_id']}/{self.attributes['index_id']}"


class AwsEksCluster(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsLbTrustStore(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsMediaStoreContainerPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["container_name"]):
            return None
        return self.attributes["container_name"]


class AwsRamSharingWithOrganization(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsNetworkmanagerLinkAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["global_network_id", "link_id", "device_id"]):
            return None
        return f"{self.attributes['global_network_id']},{self.attributes['link_id']},{self.attributes['device_id']}"


class AwsWafSqlInjectionMatchSet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsLightsailLbCertificateAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["lb_name", "certificate_name"]):
            return None
        return f"{self.attributes['lb_name']},{self.attributes['certificate_name']}"


class AwsIotDomainConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsQuicksightIamPolicyAssignment(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = ["aws_account_id", "namespace", "assignment_name"]
        if not self.has_attributes(required_attrs):
            return None

        account_id = self.attributes.get("aws_account_id", "")
        namespace = self.attributes.get("namespace", "default")
        assignment_name = self.attributes.get("assignment_name", "")

        return f"{account_id},{namespace},{assignment_name}"


class AwsGuarddutyOrganizationConfigurationFeature(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["detector_id", "name"]):
            return None
        return f"{self.attributes['detector_id']}/{self.attributes['name']}"


class AwsSecretsmanagerSecretPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("secret_arn", None)


class AwsLicensemanagerAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["resource_arn", "license_configuration_arn"]):
            return None
        return f"{self.attributes['resource_arn']},{self.attributes['license_configuration_arn']}"


class AwsVpcEndpointConnectionNotification(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsVpclatticeAccessLogSubscription(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsSesIdentityPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["identity", "name"]):
            return None
        return f"{self.attributes['identity']}|{self.attributes['name']}"


class AwsFmsAdminAccount(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("account_id", None)


class AwsRoute53recoveryreadinessReadinessCheck(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("readiness_check_name", None)


class AwsGlueCatalogDatabase(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        catalog_id = self.attributes.get(
            "catalog_id", self.attributes.get("account_id")
        )
        if not catalog_id:
            return None
        return f"{catalog_id}:{self.attributes['name']}"


class AwsIamOrganizationsFeatures(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsSagemakerEndpointConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsIamGroupPoliciesExclusive(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["group_name"]):
            return None
        return self.attributes["group_name"]


class AwsEmrInstanceFleet(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["cluster_id", "id"]):
            return None
        return f"{self.attributes['cluster_id']}/{self.attributes['id']}"


class AwsRedshiftPartner(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(
            ["account_id", "cluster_identifier", "database_name", "partner_name"]
        ):
            return None
        return f"{self.attributes['account_id']}:{self.attributes['cluster_identifier']}:{self.attributes['database_name']}:{self.attributes['partner_name']}"


class AwsKendraQuerySuggestionsBlockList(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["query_suggestions_block_list_id", "index_id"]):
            return None
        return f"{self.attributes['query_suggestions_block_list_id']}/{self.attributes['index_id']}"


class AwsLbCookieStickinessPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name", "load_balancer", "lb_port"]):
            return None
        return f"{self.attributes['load_balancer']}:{self.attributes['name']}:{self.attributes['lb_port']}"


class AwsVpcPeeringConnectionAccepter(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("vpc_peering_connection_id", None)


class AwsSesv2ContactList(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("contact_list_name", None)


class AwsNetworkmanagerGlobalNetwork(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsSnsTopicSubscription(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsSagemakerServicecatalogPortfolioStatus(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsIotAuthorizer(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsKendraExperience(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id", "index_id"]):
            return None
        return f"{self.attributes['id']}/{self.attributes['index_id']}"


class AwsTimestreamwriteDatabase(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("database_name", None)


class AwsEmrBlockPublicAccessConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        return "current"


class AwsWafregionalGeoMatchSet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsVpcSecurityGroupIngressRule(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("security_group_rule_id", None)


class AwsVpcEndpointServicePrivateDnsVerification(BaseResource):
    def _get_import_id(self) -> str | None:
        return None


class AwsTransferServer(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsSagemakerWorkforce(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["workforce_name"]):
            return None
        return self.attributes["workforce_name"]


class AwsPinpointsmsvoicev2OptOutList(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsGlueUserDefinedFunction(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = ["catalog_id", "database_name", "name"]
        if not self.has_attributes(required_attrs):
            return None

        catalog_id = self.attributes.get(
            "catalog_id", self.attributes.get("account_id")
        )
        database_name = self.attributes["database_name"]
        function_name = self.attributes["name"]

        return f"{catalog_id}:{database_name}:{function_name}"


class AwsVpcNetworkPerformanceMetricSubscription(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["source", "destination"]):
            return None
        return f"{self.attributes['source']}/{self.attributes['destination']}"


class AwsIvschatLoggingConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsStoragegatewayFileSystemAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsPinpointsmsvoicev2ConfigurationSet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsVerifiedpermissionsSchema(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("policy_store_id", None)


class AwsSchemasSchema(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name", "registry_name"]):
            return None
        return f"{self.attributes['name']}/{self.attributes['registry_name']}"


class AwsVpcIpamPoolCidrAllocation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id", "ipam_pool_id"]):
            return None
        return f"{self.attributes['id']}_{self.attributes['ipam_pool_id']}"


class AwsIamUserSshKey(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["username", "ssh_public_key_id", "encoding"]):
            return None
        return f"{self.attributes['username']}:{self.attributes['ssh_public_key_id']}:{self.attributes['encoding']}"


class AwsRekognitionStreamProcessor(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsSsmincidentsReplicationSet(BaseResource):
    def _get_import_id(self) -> str | None:
        return "import"


class AwsNetworkmanagerSite(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsSsmDocument(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsSnapshotCreateVolumePermission(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["snapshot_id", "account_id"]):
            return None
        return f"{self.attributes['snapshot_id']}-{self.attributes['account_id']}"


class AwsKmsExternalKey(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsSnsTopicDataProtectionPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsRumAppMonitor(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsSesConfigurationSet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsLambdaFunctionEventInvokeConfig(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["function_name"]):
            return None

        function_name = self.attributes["function_name"]
        qualifier = self.attributes.get("qualifier")

        if qualifier:
            return f"{function_name}:{qualifier}"

        return function_name


class AwsVpcIpamScope(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsQuicksightDataSet(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["aws_account_id", "data_set_id"]):
            return None
        return f"{self.attributes['aws_account_id']},{self.attributes['data_set_id']}"


class AwsGlueCrawler(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsIotThingType(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsTransferProfile(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("profile_id", None)


class AwsSesv2AccountSuppressionAttributes(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEmrInstanceGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["cluster_id", "id"]):
            return None
        return f"{self.attributes['cluster_id']}/{self.attributes['id']}"


class AwsWafregionalWebAclAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["web_acl_id", "resource_arn"]):
            return None
        return f"{self.attributes['web_acl_id']}:{self.attributes['resource_arn']}"


class AwsGlobalacceleratorListener(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsGlueClassifier(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsSubnet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEcrReplicationConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("registry_id", None)


class AwsSsmResourceDataSync(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsInspector2DelegatedAdminAccount(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("account_id", None)


class AwsNetworkmanagerDevice(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsGuarddutyIpset(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["detector_id", "id"]):
            return None
        return f"{self.attributes['detector_id']}:{self.attributes['id']}"


class AwsM2Environment(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsLightsailInstance(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsMedialiveInputSecurityGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsPrometheusWorkspace(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsWorklinkWebsiteCertificateAuthorityAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["fleet_arn", "website_ca_id"]):
            return None
        return f"{self.attributes['fleet_arn']},{self.attributes['website_ca_id']}"


class AwsIotThingPrincipalAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["principal", "thing"]):
            return None
        return f"{self.attributes['thing']}:{self.attributes['principal']}"


class AwsIamUserGroupMembership(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["user", "groups"]):
            return None
        groups_str = "/".join(sorted(self.attributes["groups"]))
        return f"{self.attributes['user']}/{groups_str}"


class AwsLocationGeofenceCollection(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("collection_name", None)


class AwsSpotFleetRequest(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsOpensearchserverlessVpcEndpoint(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsWafRuleGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEfsFileSystem(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsLightsailBucketAccessKey(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["bucket_name", "access_key_id"]):
            return None
        return f"{self.attributes['bucket_name']},{self.attributes['access_key_id']}"


class AwsOpensearchserverlessSecurityPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name", "type"]):
            return None
        return f"{self.attributes['name']}/{self.attributes['type']}"


class AwsLightsailLbHttpsRedirectionPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("lb_name", None)


class AwsLexv2modelsBotVersion(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["bot_id", "bot_version"]):
            return None
        return f"{self.attributes['bot_id']},{self.attributes['bot_version']}"


class AwsXrayEncryptionConfig(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsPinpointEventStream(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("application_id", None)


class AwsGrafanaWorkspaceSamlConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["workspace_id"]):
            return None
        return self.attributes["workspace_id"]


class AwsEc2TransitGatewayPolicyTable(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsQldbLedger(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsRdsClusterInstance(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["identifier"]):
            return None
        return self.attributes["identifier"]


class AwsRbinRule(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEfsAccessPoint(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsIamServerCertificate(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsS3BucketVersioning(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["bucket"]):
            return None

        if "expected_bucket_owner" in self.attributes:
            return f"{self.attributes['bucket']},{self.attributes['expected_bucket_owner']}"

        return self.attributes["bucket"]


class AwsVpclatticeResourcePolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("resource_arn", None)


class AwsVerifiedaccessGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["verifiedaccess_group_id"]):
            return None
        return self.attributes["verifiedaccess_group_id"]


class AwsGuarddutyPublishingDestination(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id", "detector_id"]):
            return None
        return f"{self.attributes['detector_id']}:{self.attributes['id']}"


class AwsEksNodeGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["cluster_name", "node_group_name"]):
            return None
        return f"{self.attributes['cluster_name']}:{self.attributes['node_group_name']}"


class AwsSfnActivity(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsImagebuilderContainerRecipe(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsKmsAlias(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsServicecatalogProductPortfolioAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["portfolio_id", "product_id"]):
            return None
        accept_language = self.attributes.get("accept_language", "en")
        return f"{accept_language}:{self.attributes['portfolio_id']}:{self.attributes['product_id']}"


class AwsSagemakerProject(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("project_name", None)


class AwsTranscribeMedicalVocabulary(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("vocabulary_name", None)


class AwsRdsCertificate(BaseResource):
    def _get_import_id(self) -> str | None:
        return "default"


class AwsElasticacheReplicationGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["replication_group_id"]):
            return None
        return self.attributes["replication_group_id"]


class AwsSagemakerFlowDefinition(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["flow_definition_name"]):
            return None
        return self.attributes["flow_definition_name"]


class AwsNetworkfirewallResourcePolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["resource_arn"]):
            return None
        return self.attributes["resource_arn"]


class AwsOpsworksStaticWebLayer(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsOpsworksRailsAppLayer(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsGlacierVault(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsPaymentcryptographyKey(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsGrafanaRoleAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["workspace_id", "role"]):
            return None
        return f"{self.attributes['workspace_id']}:{self.attributes['role']}"


class AwsServicecatalogappregistryAttributeGroupAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["application_id", "attribute_group_id"]):
            return None
        return f"{self.attributes['application_id']},{self.attributes['attribute_group_id']}"


class AwsGlueDataCatalogEncryptionSettings(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("catalog_id", self.attributes.get("id"))


class AwsNetworkmanagerTransitGatewayPeering(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsFlowLog(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsNatGateway(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsWorkspacesDirectory(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["directory_id"]):
            return None
        return self.attributes["directory_id"]


class AwsOpsworksNodejsAppLayer(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["stack_id", "id"]):
            return None
        return f"{self.attributes['stack_id']}/{self.attributes['id']}"


class AwsPinpointApnsChannel(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["application_id"]):
            return None
        return self.attributes["application_id"]


class AwsSsoadminAccountAssignment(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = [
            "principal_id",
            "principal_type",
            "target_id",
            "target_type",
            "permission_set_arn",
            "instance_arn",
        ]
        if not self.has_attributes(required_attrs):
            return None

        return ",".join(
            [
                self.attributes["principal_id"],
                self.attributes["principal_type"],
                self.attributes["target_id"],
                self.attributes["target_type"],
                self.attributes["permission_set_arn"],
                self.attributes["instance_arn"],
            ]
        )


class AwsMacie2ClassificationJob(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsGameliftFleet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsSesEventDestination(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["configuration_set_name", "name"]):
            return None
        return f"{self.attributes['configuration_set_name']}/{self.attributes['name']}"


class AwsPaymentcryptographyKeyAlias(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["alias_name"]):
            return None
        return self.attributes["alias_name"]


class AwsGlueJob(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsMacie2Member(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["account_id"]):
            return None
        return self.attributes["account_id"]


class AwsLightsailDomainEntry(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = ["name", "domain_name", "type", "target"]
        if not self.has_attributes(required_attrs):
            return None
        return f"{self.attributes['name']},{self.attributes['domain_name']},{self.attributes['type']},{self.attributes['target']}"


class AwsSagemakerSpace(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes["arn"] if self.has_attributes(["arn"]) else None


class AwsS3ObjectCopy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["bucket", "key"]):
            return None
        return f"{self.attributes['bucket']}/{self.attributes['key']}"


class AwsMacie2ClassificationExportConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsWorklinkFleet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsSecuritylakeSubscriber(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsVpcBlockPublicAccessOptions(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("aws_region", None)


class AwsSecurityhubStandardsSubscription(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["standards_arn"]):
            return None
        return self.attributes["standards_arn"]


class AwsIotLoggingOptions(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["role_arn"]):
            return None
        return "default"


class AwsS3BucketAccelerateConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["bucket"]):
            return None

        if (
            "expected_bucket_owner" in self.attributes
            and self.attributes["expected_bucket_owner"]
        ):
            return f"{self.attributes['bucket']},{self.attributes['expected_bucket_owner']}"

        return self.attributes["bucket"]


class AwsS3BucketIntelligentTieringConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["bucket", "name"]):
            return None
        return f"{self.attributes['bucket']}:{self.attributes['name']}"


class AwsQuicksightTemplateAlias(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = ["aws_account_id", "template_id", "alias_name"]
        if not self.has_attributes(required_attrs):
            return None

        account_id = self.attributes.get("aws_account_id", "")
        template_id = self.attributes["template_id"]
        alias_name = self.attributes["alias_name"]

        return f"{account_id},{template_id},{alias_name}"


class AwsEksFargateProfile(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["cluster_name", "fargate_profile_name"]):
            return None
        return f"{self.attributes['cluster_name']}:{self.attributes['fargate_profile_name']}"


class AwsEmrcontainersJobTemplate(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsRamResourceShareAccepter(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("share_arn", None)


class AwsIotEventConfigurations(BaseResource):
    pass


class AwsSignerSigningProfilePermission(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["profile_name", "statement_id"]):
            return None
        return f"{self.attributes['profile_name']}/{self.attributes['statement_id']}"


class AwsMemorydbSubnetGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsNetworkmanagerAttachmentAccepter(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["attachment_id", "attachment_type"]):
            return None
        return (
            f"{self.attributes['attachment_id']},{self.attributes['attachment_type']}"
        )


class AwsLakeformationPermissions(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["principal", "permissions"]):
            return None

        # Determine the specific resource type and construct import ID
        resource_types = [
            "catalog_resource",
            "data_cells_filter",
            "data_location",
            "database",
            "lf_tag",
            "lf_tag_policy",
            "table",
            "table_with_columns",
        ]

        for resource_type in resource_types:
            if resource_type in self.attributes:
                # Use principal and resource details for import ID
                return f"{self.attributes['principal']}/{resource_type}"

        return None


class AwsMemorydbUser(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("user_name", None)


class AwsEksAddon(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["cluster_name", "addon_name"]):
            return None
        return f"{self.attributes['cluster_name']}:{self.attributes['addon_name']}"


class AwsRdsClusterSnapshotCopy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["target_db_cluster_snapshot_identifier"]):
            return None
        return self.attributes["target_db_cluster_snapshot_identifier"]


class AwsS3BucketAcl(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["bucket"]):
            return None

        parts = [self.attributes["bucket"]]

        if "expected_bucket_owner" in self.attributes:
            parts.append(self.attributes["expected_bucket_owner"])

        if "acl" in self.attributes:
            parts.append(self.attributes["acl"])

        return ",".join(parts)


class AwsKinesisVideoStream(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsS3BucketWebsiteConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["bucket"]):
            return None

        if "expected_bucket_owner" in self.attributes:
            return f"{self.attributes['bucket']},{self.attributes['expected_bucket_owner']}"

        return self.attributes["bucket"]


class AwsSesv2DedicatedIpAssignment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["ip", "destination_pool_name"]):
            return None
        return f"{self.attributes['ip']},{self.attributes['destination_pool_name']}"


class AwsWafv2WebAclLoggingConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["resource_arn"]):
            return None
        return self.attributes["resource_arn"]


class AwsRoute53CidrCollection(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsKmsKeyPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["key_id"]):
            return None
        return self.attributes["key_id"]


class AwsInspector2MemberAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("account_id", None)


class AwsSsmincidentsResponsePlan(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsMskconnectCustomPlugin(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsNeptuneClusterParameterGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsNetworkmanagerConnectAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsFsxOpenzfsFileSystem(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsKinesisStreamConsumer(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsRedshiftEndpointAuthorization(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["account", "cluster_identifier"]):
            return None
        return f"{self.attributes['account']}:{self.attributes['cluster_identifier']}"


class AwsNeptuneClusterInstance(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsRoute53profilesAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsKinesisanalyticsv2Application(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsSsmcontactsPlan(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["contact_id"]):
            return None
        return self.attributes["contact_id"]


class AwsStoragegatewayGateway(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsVpclatticeListenerRule(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(
            ["service_identifier", "listener_identifier", "rule_id"]
        ):
            return None
        return f"{self.attributes['service_identifier']}/{self.attributes['listener_identifier']}/{self.attributes['rule_id']}"


class AwsServerlessapplicationrepositoryCloudformationStack(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None

        name = self.attributes["name"]
        return (
            f"serverlessrepo-{name}" if not name.startswith("serverlessrepo-") else name
        )


class AwsServicecatalogTagOptionResourceAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["tag_option_id", "resource_id"]):
            return None
        return f"{self.attributes['tag_option_id']}:{self.attributes['resource_id']}"


class AwsMacie2FindingsFilter(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsResourceexplorer2Index(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsIotCaCertificate(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsWafGeoMatchSet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsWafByteMatchSet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsRoute53ResolverEndpoint(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsRekognitionProject(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsRoute53profilesResourceAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsKinesisanalyticsv2ApplicationSnapshot(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["application_name", "snapshot_name"]):
            return None
        return (
            f"{self.attributes['application_name']}/{self.attributes['snapshot_name']}"
        )


class AwsFinspaceKxDataview(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["environment_id", "database_name", "name"]):
            return None
        return f"{self.attributes['environment_id']},{self.attributes['database_name']},{self.attributes['name']}"


class AwsTransferCertificate(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("certificate_id", None)


class AwsMediaConvertQueue(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsWafRegexPatternSet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEc2TransitGatewayPolicyTableAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(
            ["transit_gateway_policy_table_id", "transit_gateway_attachment_id"]
        ):
            return None
        return f"{self.attributes['transit_gateway_policy_table_id']}_{self.attributes['transit_gateway_attachment_id']}"


class AwsSchemasDiscoverer(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsLbListenerCertificate(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["listener_arn", "certificate_arn"]):
            return None
        return f"{self.attributes['listener_arn']}_{self.attributes['certificate_arn']}"


class AwsEvidentlyProject(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsSsoadminPermissionsBoundaryAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["permission_set_arn", "instance_arn"]):
            return None
        return (
            f"{self.attributes['permission_set_arn']},{self.attributes['instance_arn']}"
        )


class AwsSagemakerHumanTaskUi(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("human_task_ui_name", None)


class AwsStoragegatewayUploadBuffer(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["gateway_arn", "disk_id", "disk_path"]):
            return None

        disk_identifier = self.attributes.get("disk_id") or self.attributes.get(
            "disk_path"
        )
        if not disk_identifier:
            return None

        return f"{self.attributes['gateway_arn']}:{disk_identifier}"


class AwsSsmquicksetupConfigurationManager(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("manager_arn", None)


class AwsMemorydbParameterGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsFsxLustreFileSystem(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsS3controlAccessGrantsLocation(BaseResource):
    def _get_import_id(self) -> str | None:
        account_id = self.attributes.get("account_id")
        location_id = self.attributes.get("access_grants_location_id")

        if not account_id or not location_id:
            return None

        return f"{account_id},{location_id}"


class AwsVpcIpv6CidrBlockAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsS3BucketOwnershipControls(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("bucket", None)


class AwsS3BucketLogging(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["bucket"]):
            return None

        if self.attributes.get("expected_bucket_owner"):
            return f"{self.attributes['bucket']},{self.attributes['expected_bucket_owner']}"

        return self.attributes["bucket"]


class AwsWafregionalRegexPatternSet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsRoute53ResolverFirewallDomainList(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsLightsailStaticIpAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["static_ip_name", "instance_name"]):
            return None
        return f"{self.attributes['static_ip_name']},{self.attributes['instance_name']}"


class AwsRedshiftDataShareAuthorization(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["data_share_arn", "consumer_identifier"]):
            return None
        return f"{self.attributes['data_share_arn']},{self.attributes['consumer_identifier']}"


class AwsSesDomainDkim(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("domain", None)


class AwsRedshiftserverlessWorkgroup(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["workgroup_name"]):
            return None
        return self.attributes["workgroup_name"]


class AwsMskServerlessCluster(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsServicecatalogProvisionedProduct(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsIamOpenidConnectProvider(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsFsxOntapStorageVirtualMachine(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsIvsRecordingConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsLocationMap(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("map_name", None)


class AwsSchemasRegistryPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["registry_name"]):
            return None
        return self.attributes["registry_name"]


class AwsSagemakerModelPackageGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("model_package_group_name", None)


class AwsProxyProtocolPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["load_balancer", "instance_ports"]):
            return None
        return self.attributes["load_balancer"]


class AwsPinpointApp(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("application_id", None)


class AwsSagemakerCodeRepository(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["code_repository_name"]):
            return None
        return self.attributes["code_repository_name"]


class AwsSsmDefaultPatchBaseline(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["baseline_id", "operating_system"]):
            return None

        # Prioritize baseline_id if available
        if self.attributes.get("baseline_id"):
            return self.attributes["baseline_id"]

        # Fallback to operating system
        return self.attributes.get("operating_system")


class AwsFsxOpenzfsVolume(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsLambdaAlias(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["function_name", "name"]):
            return None
        return f"{self.attributes['function_name']}/{self.attributes['name']}"


class AwsIotIndexingConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        return ""


class AwsQuicksightAnalysis(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["aws_account_id", "analysis_id"]):
            return None
        return f"{self.attributes.get('aws_account_id', '')},{self.attributes['analysis_id']}"


class AwsSecretsmanagerSecretRotation(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsTransferSshKey(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["server_id", "user_name", "ssh_public_key_id"]):
            return None
        return f"{self.attributes['server_id']}/{self.attributes['user_name']}/{self.attributes['ssh_public_key_id']}"


class AwsSagemakerDomain(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsNeptuneGlobalCluster(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("global_cluster_identifier", None)


class AwsRdsClusterParameterGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsSsmAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("association_id", None)


class AwsNetworkmanagerSiteToSiteVpnAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsS3controlAccessPointPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["access_point_arn"]):
            return None
        return self.attributes["access_point_arn"]


class AwsResourcegroupsGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsImagebuilderImagePipeline(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsLaunchTemplate(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsWafIpset(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsNetworkmonitorProbe(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["monitor_name", "arn"]):
            return None

        monitor_name = self.attributes.get("monitor_name")
        probe_id = self.attributes.get("arn", "").split("/")[-1]

        return f"{monitor_name},{probe_id}"


class AwsIamSecurityTokenServicePreferences(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsMqConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsGlueDataQualityRuleset(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsEcrpublicRepositoryPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["repository_name"]):
            return None
        return self.attributes["repository_name"]


class AwsM2Application(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("application_id", None)


class AwsGrafanaWorkspaceServiceAccountToken(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["workspace_id", "service_account_token_id"]):
            return None
        return f"{self.attributes['workspace_id']}/{self.attributes['service_account_token_id']}"


class AwsS3BucketNotification(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["bucket"]):
            return None
        return self.attributes["bucket"]


class AwsServicecatalogBudgetResourceAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["budget_name", "resource_id"]):
            return None
        return f"{self.attributes['budget_name']}:{self.attributes['resource_id']}"


class AwsWafregionalByteMatchSet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsGlacierVaultLock(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["vault_name"]):
            return None
        return self.attributes["vault_name"]


class AwsGlueSecurityConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsNetworkmanagerCoreNetworkPolicyAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["core_network_id"]):
            return None
        return self.attributes["core_network_id"]


class AwsRoute53QueryLog(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsInspectorAssessmentTarget(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsTransferAgreement(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["server_id", "agreement_id"]):
            return None
        return f"{self.attributes['server_id']}/{self.attributes['agreement_id']}"


class AwsMskconnectConnector(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsSecuritylakeSubscriberNotification(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["subscriber_id"]):
            return None
        return self.attributes["subscriber_id"]


class AwsSagemakerModelPackageGroupPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("model_package_group_name", None)


class AwsSyntheticsGroupAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["canary_arn", "group_name"]):
            return None
        return f"{self.attributes['canary_arn']},{self.attributes['group_name']}"


class AwsSagemakerImageVersion(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("image_name", None)


class AwsIamRolePoliciesExclusive(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["role_name"]):
            return None
        return self.attributes["role_name"]


class AwsMskVpcConnection(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsGameliftGameServerGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["game_server_group_name"]):
            return None
        return self.attributes["game_server_group_name"]


class AwsVerifiedaccessInstanceLoggingConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["verifiedaccess_instance_id"]):
            return None
        return self.attributes["verifiedaccess_instance_id"]


class AwsOpensearchAuthorizeVpcEndpointAccess(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["domain_name", "account"]):
            return None
        return f"{self.attributes['domain_name']}/{self.attributes['account']}"


class AwsServicecatalogProvisioningArtifact(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["provisioning_artifact_id", "product_id"]):
            return None
        return f"{self.attributes['provisioning_artifact_id']}:{self.attributes['product_id']}"


class AwsNeptuneSubnetGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsOpensearchserverlessAccessPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name", "type"]):
            return None
        return f"{self.attributes['name']}/{self.attributes['type']}"


class AwsLambdaFunctionRecursionConfig(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["function_name"]):
            return None
        return self.attributes["function_name"]


class AwsMwaaEnvironment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsFisExperimentTemplate(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsRoute53recoveryreadinessCell(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("cell_name", None)


class AwsServicecatalogConstraint(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsRedshiftserverlessEndpointAccess(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("endpoint_name", None)


class AwsNetworkInterfaceAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["attachment_id"]):
            return None
        return self.attributes["attachment_id"]


class AwsMskReplicator(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsSecuritylakeCustomLogSource(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("source_name", None)


class AwsSwfDomain(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsVpcEndpointRouteTableAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["vpc_endpoint_id", "route_table_id"]):
            return None
        return (
            f"{self.attributes['vpc_endpoint_id']}/{self.attributes['route_table_id']}"
        )


class AwsShieldProactiveEngagement(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("account_id", None)


class AwsLambdaInvocation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["function_name"]):
            return None

        function_name = self.attributes["function_name"]
        qualifier = self.attributes.get("qualifier", "$LATEST")

        return f"{function_name}:{qualifier}"


class AwsOpsworksGangliaLayer(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsKendraIndex(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsLakeformationDataLakeSettings(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("catalog_id", "default")


class AwsRedshiftserverlessCustomDomainAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["workgroup_name", "custom_domain_name"]):
            return None
        return f"{self.attributes['workgroup_name']},{self.attributes['custom_domain_name']}"


class AwsNetworkmanagerTransitGatewayRegistration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["global_network_id", "transit_gateway_arn"]):
            return None
        return f"{self.attributes['global_network_id']},{self.attributes['transit_gateway_arn']}"


class AwsGrafanaLicenseAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("workspace_id", None)


class AwsWafregionalRule(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsQuicksightDashboard(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["aws_account_id", "dashboard_id"]):
            return None
        account_id = self.attributes.get("aws_account_id", "")
        dashboard_id = self.attributes.get("dashboard_id", "")
        return f"{account_id},{dashboard_id}"


class AwsSagemakerNotebookInstance(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsLambdaLayerVersionPermission(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["layer_name", "version_number"]):
            return None
        return f"{self.attributes['layer_name']},{self.attributes['version_number']}"


class AwsVerifiedaccessInstanceTrustProviderAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(
            ["verifiedaccess_instance_id", "verifiedaccess_trust_provider_id"]
        ):
            return None
        return f"{self.attributes['verifiedaccess_instance_id']}/{self.attributes['verifiedaccess_trust_provider_id']}"


class AwsSecurityhubStandardsControlAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["standards_arn", "security_control_id"]):
            return None
        return f"{self.attributes['standards_arn']}|{self.attributes['security_control_id']}"


class AwsEcsTaskDefinition(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsRouteTableAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if self.has_attributes(["subnet_id", "route_table_id"]):
            return f"{self.attributes['subnet_id']}/{self.attributes['route_table_id']}"
        elif self.has_attributes(["gateway_id", "route_table_id"]):
            return (
                f"{self.attributes['gateway_id']}/{self.attributes['route_table_id']}"
            )
        return None


class AwsPinpointAdmChannel(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["application_id"]):
            return None
        return self.attributes["application_id"]


class AwsXrayGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsGluePartitionIndex(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = ["database_name", "table_name", "partition_index"]
        if not self.has_attributes(required_attrs):
            return None

        catalog_id = self.attributes.get("catalog_id", "").strip() or ""
        database_name = self.attributes["database_name"]
        table_name = self.attributes["table_name"]
        index_name = self.attributes["partition_index"][0]["index_name"]

        if catalog_id:
            return f"{catalog_id}:{database_name}:{table_name}:{index_name}"
        return f"{database_name}:{table_name}:{index_name}"


class AwsMedialiveChannel(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("channel_id", None)


class AwsOpsworksStack(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsSecurityhubOrganizationConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsSpotDatafeedSubscription(BaseResource):
    def _get_import_id(self) -> str | None:
        return "spot-datafeed-subscription"


class AwsServiceDiscoveryInstance(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["service_id", "instance_id"]):
            return None
        return f"{self.attributes['service_id']}/{self.attributes['instance_id']}"


class AwsGlueWorkflow(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsFinspaceKxScalingGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["environment_id", "name"]):
            return None
        return f"{self.attributes['environment_id']},{self.attributes['name']}"


class AwsFsxWindowsFileSystem(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsStoragegatewayNfsFileShare(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsSsmPatchGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["patch_group", "baseline_id"]):
            return None
        return f"{self.attributes['patch_group']},{self.attributes['baseline_id']}"


class AwsWafregionalRuleGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsLightsailInstancePublicPorts(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["instance_name"]):
            return None
        return self.attributes["instance_name"]


class AwsWafRegexMatchSet(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsMacie2CustomDataIdentifier(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsImagebuilderComponent(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsLambdaCodeSigningConfig(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsVpcSecurityGroupVpcAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["security_group_id", "vpc_id"]):
            return None
        return f"{self.attributes['security_group_id']},{self.attributes['vpc_id']}"


class AwsRoute53recoverycontrolconfigSafetyRule(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsS3controlObjectLambdaAccessPointPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        account_id = self.attributes.get("account_id")
        name = self.attributes.get("name")

        if not account_id or not name:
            return None

        return f"{account_id}:{name}"


class AwsS3BucketPublicAccessBlock(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("bucket", None)


class AwsVerifiedpermissionsPolicyStore(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("policy_store_id", None)


class AwsRedshiftResourcePolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("resource_arn", None)


class AwsShieldSubscription(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEfsFileSystemPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("file_system_id", None)


class AwsEfsBackupPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("file_system_id", None)


class AwsGlueMlTransform(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsPrometheusScraper(BaseResource):
    def _get_import_id(self) -> str | None:
        return (
            self.attributes.get("arn", "").split("/")[-1]
            if "arn" in self.attributes
            else None
        )


class AwsRoute53ResolverDnssecConfig(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsNetworkmanagerConnectPeer(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsOpsworksPermission(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["stack_id", "user_arn"]):
            return None
        return f"{self.attributes['stack_id']}/{self.attributes['user_arn']}"


class AwsVpcSecurityGroupEgressRule(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("security_group_rule_id", None)


class AwsEcsCapacityProvider(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsOpensearchDomainSamlOptions(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["domain_name"]):
            return None
        return self.attributes["domain_name"]


class AwsS3tablesNamespace(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["table_bucket_arn", "namespace"]):
            return None
        return f"{self.attributes['table_bucket_arn']};{self.attributes['namespace']}"


class AwsOpsworksMemcachedLayer(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id", "stack_id"]):
            return None
        return self.attributes["id"]


class AwsKmsCustomKeyStore(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsWafregionalRateBasedRule(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsLocationTrackerAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["tracker_name", "consumer_arn"]):
            return None
        return f"{self.attributes['tracker_name']}|{self.attributes['consumer_arn']}"


class AwsImagebuilderWorkflow(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsRedshiftLogging(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["cluster_identifier"]):
            return None
        return self.attributes["cluster_identifier"]


class AwsSnsSmsPreferences(BaseResource):
    def _get_import_id(self) -> str | None:
        return None  # Import is not supported for this resource


class AwsSagemakerDataQualityJobDefinition(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsOpensearchserverlessCollection(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEc2TransitGatewayRouteTableAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(
            ["transit_gateway_route_table_id", "transit_gateway_attachment_id"]
        ):
            return None
        return f"{self.attributes['transit_gateway_route_table_id']}_{self.attributes['transit_gateway_attachment_id']}"


class AwsIamRolePolicyAttachmentsExclusive(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["role_name"]):
            return None
        return self.attributes["role_name"]


class AwsTransferAccess(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["server_id", "external_id"]):
            return None
        return f"{self.attributes['server_id']}/{self.attributes['external_id']}"


class AwsElasticacheUserGroupAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["user_group_id", "user_id"]):
            return None
        return f"{self.attributes['user_group_id']},{self.attributes['user_id']}"


class AwsNetworkfirewallLoggingConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["firewall_arn"]):
            return None
        return self.attributes["firewall_arn"]


class AwsEc2TransitGatewayPrefixListReference(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(
            ["transit_gateway_route_table_id", "prefix_list_id"]
        ):
            return None
        return f"{self.attributes['transit_gateway_route_table_id']}_{self.attributes['prefix_list_id']}"


class AwsEvidentlyLaunch(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name", "project"]):
            return None
        return f"{self.attributes['name']}:{self.attributes['project']}"


class AwsRedshiftClusterIamRoles(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["cluster_identifier"]):
            return None
        return self.attributes["cluster_identifier"]


class AwsOpsworksHaproxyLayer(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsElasticBeanstalkApplicationVersion(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["application", "name"]):
            return None
        return f"{self.attributes['application']}/{self.attributes['name']}"


class AwsNeptuneParameterGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsGlueTrigger(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsOpsworksMysqlLayer(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsMqBroker(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsNetworkAclAssociation(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsRoute53CidrLocation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["cidr_collection_id", "name"]):
            return None
        return f"{self.attributes['cidr_collection_id']},{self.attributes['name']}"


class AwsRedshiftEventSubscription(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsSpotInstanceRequest(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEgressOnlyInternetGateway(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsIamUserPolicyAttachmentsExclusive(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["user_name"]):
            return None
        return self.attributes["user_name"]


class AwsSagemakerFeatureGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["feature_group_name"]):
            return None
        return self.attributes["feature_group_name"]


class AwsLbTrustStoreRevocation(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["trust_store_arn", "revocation_id"]):
            return None
        return (
            f"{self.attributes['trust_store_arn']},{self.attributes['revocation_id']}"
        )


class AwsSagemakerNotebookInstanceLifecycleConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsImagebuilderDistributionConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsOpsworksEcsClusterLayer(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsNetworkfirewallTlsInspectionConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsSesDomainMailFrom(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("domain", None)


class AwsMacie2Account(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsQuicksightTheme(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["aws_account_id", "theme_id"]):
            return None
        return (
            f"{self.attributes.get('aws_account_id')},{self.attributes.get('theme_id')}"
        )


class AwsS3BucketRequestPaymentConfiguration(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["bucket"]):
            return None

        if self.attributes.get("expected_bucket_owner"):
            return f"{self.attributes['bucket']},{self.attributes['expected_bucket_owner']}"

        return self.attributes["bucket"]


class AwsKendraThesaurus(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsElasticsearchDomainPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["domain_name"]):
            return None
        return self.attributes["domain_name"]


class AwsServicecatalogOrganizationsAccess(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsSignerSigningJob(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("job_id", None)


class AwsEcsAccountSettingDefault(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsPlacementGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsAppCookieStickinessPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name", "load_balancer", "lb_port"]):
            return None
        return f"{self.attributes['load_balancer']}:{self.attributes['lb_port']}:{self.attributes['name']}"


class AwsAthenaDatabase(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsDbInstance(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["identifier"]):
            return None
        return self.attributes["identifier"]


class AwsEc2TransitGatewayRoute(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(
            ["transit_gateway_route_table_id", "destination_cidr_block"]
        ):
            return None
        return f"{self.attributes['transit_gateway_route_table_id']}_{self.attributes['destination_cidr_block']}"


class AwsEc2TransitGatewayVpcAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsEcrRepository(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsEcrpublicRepository(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("repository_name", None)


class AwsEcsCluster(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsEip(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("allocation_id", None)


class AwsEmrStudio(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsGlueCatalogTable(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["database_name", "name"]):
            return None

        catalog_id = self.attributes.get(
            "catalog_id", self.attributes.get("aws_account_id")
        )

        return (
            f"{catalog_id}:{self.attributes['database_name']}:{self.attributes['name']}"
        )


class AwsGrafanaWorkspace(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsGrafanaWorkspaceServiceAccount(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["workspace_id", "service_account_id"]):
            return None
        return (
            f"{self.attributes['workspace_id']},{self.attributes['service_account_id']}"
        )


class AwsGuarddutyDetector(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsIamGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsIamGroupPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["group", "name"]):
            return None
        return f"{self.attributes['group']}:{self.attributes['name']}"


class AwsIamGroupPolicyAttachment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["group", "policy_arn"]):
            return None
        return f"{self.attributes['group']}/{self.attributes['policy_arn']}"


class AwsIamRole(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsIamRolePolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["role", "name"]):
            return None
        return f"{self.attributes['role']}:{self.attributes['name']}"


class AwsIamUser(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsIdentitystoreGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["identity_store_id", "group_id"]):
            return None
        return f"{self.attributes['identity_store_id']}/{self.attributes['group_id']}"


class AwsImagebuilderImage(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsInternetGateway(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsIotPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsIotThing(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsIotThingGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsIotTopicRule(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsLakeformationResourceLfTag(BaseResource):
    def _get_import_id(self) -> str | None:
        return None


class AwsLambdaFunction(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["function_name"]):
            return None
        return self.attributes["function_name"]


class AwsLb(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsLbListener(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsLexBot(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name"]):
            return None
        return self.attributes["name"]


class AwsLexv2modelsBot(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsLicensemanagerGrant(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsLightsailBucket(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsLightsailContainerService(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsLightsailLb(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsMediaStoreContainer(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsMedialiveInput(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsMedialiveMultiplex(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsNeptuneCluster(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("cluster_identifier", None)


class AwsNetworkAcl(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsNetworkfirewallFirewall(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn"]):
            return None
        return self.attributes["arn"]


class AwsOamSink(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsOpensearchDomain(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["domain_name"]):
            return None
        return self.attributes["domain_name"]


class AwsOpensearchPackage(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsOrganizationsOrganization(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsQuicksightTemplate(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["aws_account_id", "template_id"]):
            return None
        return f"{self.attributes.get('aws_account_id', '')},{self.attributes.get('template_id', '')}"


class AwsRamResourceShare(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsRedshiftSnapshotCopy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("cluster_identifier", None)


class AwsRedshiftSnapshotSchedule(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("identifier", None)


class AwsRoute(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["route_table_id"]):
            return None

        destination = (
            self.attributes.get("destination_cidr_block")
            or self.attributes.get("destination_ipv6_cidr_block")
            or self.attributes.get("destination_prefix_list_id")
        )

        if not destination:
            return None

        return f"{self.attributes['route_table_id']}_{destination}"


class AwsRoute53ResolverFirewallRuleGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsRoute53ResolverQueryLogConfig(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsRoute53ResolverRule(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsRoute53TrafficPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id", "version"]):
            return None
        return f"{self.attributes['id']}/{self.attributes['version']}"


class AwsRoute53Zone(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("zone_id", None)


class AwsSagemakerApp(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes["arn"] if self.has_attributes(["arn"]) else None


class AwsSagemakerDevice(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["device_fleet_name", "device"]):
            return None
        device_name = self.attributes["device"].get("device_name", "")
        return f"{self.attributes['device_fleet_name']}/{device_name}"


class AwsSchedulerSchedule(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name", "group_name"]):
            return None
        group_name = self.attributes.get("group_name", "default")
        return f"{group_name}/{self.attributes['name']}"


class AwsSecretsmanagerSecret(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsSecurityGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsSecurityhubConfigurationPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsSecurityhubStandardsControl(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["standards_control_arn"]):
            return None
        return self.attributes["standards_control_arn"]


class AwsServicecatalogPortfolio(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsServicecatalogProduct(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsServicequotasTemplate(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["region", "quota_code", "service_code"]):
            return None
        return f"{self.attributes['region']},{self.attributes['quota_code']},{self.attributes['service_code']}"


class AwsSesReceiptRule(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["name", "rule_set_name"]):
            return None
        return f"{self.attributes['rule_set_name']}:{self.attributes['name']}"


class AwsSesv2ConfigurationSet(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["configuration_set_name"]):
            return None
        return self.attributes["configuration_set_name"]


class AwsSesv2EmailIdentity(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["email_identity"]):
            return None
        return self.attributes["email_identity"]


class AwsSnsTopic(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsSqsQueue(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("url", None)


class AwsSsmcontactsContact(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("arn", None)


class AwsSsoadminApplication(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["application_arn"]):
            return None
        return self.attributes["application_arn"]


class AwsSsoadminApplicationAssignment(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(
            ["application_arn", "principal_id", "principal_type"]
        ):
            return None
        return f"{self.attributes['application_arn']},{self.attributes['principal_id']},{self.attributes['principal_type']}"


class AwsSsoadminPermissionSet(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["arn", "instance_arn"]):
            return None
        return f"{self.attributes['arn']},{self.attributes['instance_arn']}"


class AwsStoragegatewayCache(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["gateway_arn", "disk_id"]):
            return None
        return f"{self.attributes['gateway_arn']}:{self.attributes['disk_id']}"


class AwsSyntheticsGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("name", None)


class AwsTranscribeVocabulary(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("vocabulary_name", None)


class AwsVerifiedpermissionsPolicy(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["policy_id", "policy_store_id"]):
            return None
        return f"{self.attributes['policy_id']},{self.attributes['policy_store_id']}"


class AwsVpc(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsVpcDhcpOptions(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsVpcEndpoint(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsVpcEndpointService(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsVpcIpam(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsVpcIpamPoolCidr(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["cidr", "ipam_pool_id"]):
            return None
        return f"{self.attributes['cidr']}_{self.attributes['ipam_pool_id']}"


class AwsVpclatticeListener(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["service_identifier", "listener_id"]):
            return None
        return (
            f"{self.attributes['service_identifier']}/{self.attributes['listener_id']}"
        )


class AwsVpclatticeService(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("id", None)


class AwsVpclatticeTargetGroup(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsVpnConnection(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id"]):
            return None
        return self.attributes["id"]


class AwsWafv2WebAcl(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["id", "name", "scope"]):
            return None
        return f"{self.attributes['id']}/{self.attributes['name']}/{self.attributes['scope']}"


class AwsS3Bucket(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("bucket", None)


class AwsS3BucketObject(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["bucket", "key"]):
            return None
        return f"{self.attributes['bucket']}/{self.attributes['key']}"


class AwsS3controlAccessGrantsInstance(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes.get("account_id") or self.attributes.get(
            "aws_account_id"
        )


class AwsS3controlMultiRegionAccessPoint(BaseResource):
    def _get_import_id(self) -> str | None:
        if not self.has_attributes(["account_id", "details"]):
            return None

        account_id = self.attributes.get("account_id")
        name = self.attributes["details"].get("name")

        if not account_id or not name:
            return None

        return f"{account_id}:{name}"


class AwsS3tablesTable(BaseResource):
    def _get_import_id(self) -> str | None:
        required_attrs = ["table_bucket_arn", "namespace", "name"]
        if not self.has_attributes(required_attrs):
            return None
        return f"{self.attributes['table_bucket_arn']};{self.attributes['namespace']};{self.attributes['name']}"


class AwsS3tablesTableBucket(BaseResource):
    def _get_import_id(self) -> str | None:
        return self.attributes["arn"] if self.has_attributes(["arn"]) else None
