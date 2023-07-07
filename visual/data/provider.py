# Class that is responsible to read appropriate data and return it to the app
import json


class DataProvider:
    # Read data from file
    def __init__(self, source_name):
        # Read file from source
        try:
            with open(f"{source_name}.json", "r") as f:
                self.content = json.loads(f.read())
                self.nodes = self.content['nodes']
                self.relations = self.content['relations']
                self.current_node = self.content['root']
                return
        except:
            raise Exception(f"Could not read file {source_name}.json")

    # Get subtopics of current node
    def get_sub_topics(self):
        # Get current node
        current_node = self.current_node
        # Get all sub topics
        child_nodes_ids = [rel['child'] for rel in self.relations if rel['parent'] == current_node]
        child_nodes = [node for node in self.nodes if node['id'] in child_nodes_ids]
        return child_nodes

    # Set current node to selected node
    def select_node(self, node_id):
        self.current_node = node_id

    def get_selected_node_id(self):
        return self.current_node




