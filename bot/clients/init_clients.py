from bot.clients.customs import CustomsClient
from bot.clients.storage import Storage

storage_client = Storage()
gs_client = CustomsClient()

# if __name__ == "__main__":
#     gs_client = CustomsClient()
#     print(gs_client.make_custom_worksheet("Вего"))