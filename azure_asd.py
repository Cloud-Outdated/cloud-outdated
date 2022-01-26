from azure.core.pipeline import PipelineContext, PipelineRequest
from azure.core.pipeline.policies import BearerTokenCredentialPolicy
from azure.core.pipeline.transport import HttpRequest
from azure.identity import ClientSecretCredential, DefaultAzureCredential
from azure.mgmt.redis import RedisManagementClient
from azure.mgmt.redis.models import RedisCreateParameters
from msrest.authentication import BasicTokenAuthentication


class AzureIdentityCredentialAdapter(BasicTokenAuthentication):
    def __init__(
        self,
        credential=None,
        resource_id="https://management.azure.com/.default",
        **kwargs
    ):
        """Adapt any azure-identity credential to work with SDK that needs azure.common.credentials or msrestazure.
        Default resource is ARM (syntax of endpoint v2)
        :param credential: Any azure-identity credential (DefaultAzureCredential by default)
        :param str resource_id: The scope to use to get the token (default ARM)
        """
        super(AzureIdentityCredentialAdapter, self).__init__(None)
        if credential is None:
            credential = DefaultAzureCredential()
        self._policy = BearerTokenCredentialPolicy(credential, resource_id, **kwargs)

    def _make_request(self):
        return PipelineRequest(
            HttpRequest("AzureIdentityCredentialAdapter", "https://fakeurl"),
            PipelineContext(None),
        )

    def set_token(self):
        """Ask the azure-core BearerTokenCredentialPolicy policy to get a token.
        Using the policy gives us for free the caching system of azure-core.
        We could make this code simpler by using private method, but by definition
        I can't assure they will be there forever, so mocking a fake call to the policy
        to extract the token, using 100% public API."""
        request = self._make_request()
        self._policy.on_request(request)
        # Read Authorization, and get the second part after Bearer
        token = request.http_request.headers["Authorization"].split(" ", 1)[1]
        self.token = {"access_token": token}

    def signed_session(self, session=None):
        self.set_token()
        return super(AzureIdentityCredentialAdapter, self).signed_session(session)


subscription_id = "b3f17067-22e0-4936-98ab-207fcd6a6b88"
tenant_id = "e5602cfe-945f-4396-bdd4-c66da0b94369"
client_id = "ac91b648-b115-4f44-9d9d-838c850720c9"
client_secret = "2Y57Q~W44Q-X4HTEfCXEyAbgm-yUBVhQ4oTol"

credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret,
)

wrapped_credential = AzureIdentityCredentialAdapter(credential)

redis_mgmt = RedisManagementClient(wrapped_credential, subscription_id)

for op in redis_mgmt.operations.list():
    print(op.as_dict())

print(list(redis_mgmt.redis.list()))
# subscription = next(subscription_client.subscriptions.list())
# print(subscription.subscription_id)
