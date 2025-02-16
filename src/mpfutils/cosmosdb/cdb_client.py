from azure.cosmos import CosmosClient
import logging
import os

logger = logging.getLogger("mpf-utils.cosmosdb")

class CosmosDBContainer:

    def __init__(self, database_name:str, container_name:str, endpoint:str = None, key:str = None):
        if not endpoint:
            endpoint = os.getenv("COSMOSDB_ENDPOINT")
        
        if not key:
            key = os.getenv("COSMOSDB_KEY")
        
        client = CosmosClient(endpoint, key)
        database = client.get_database_client(database_name)
        self.container = database.get_container_client(container_name)

    def run_query(self, query:str, parameters:list = None, results_as_list: bool = True):
        if not parameters:
            parameters = []

        try:
            items = self.container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=True,
            )
            if results_as_list:
                return list(items)
            else:
                return items
        except Exception as e:
            logger.error(f"Error in CosmosDBContainer: {e}")
            return None
