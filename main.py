import argparse, os, asyncio
from broker import Broker
from tools.onedrive_reader import OnedriveReader
from graph.client import GraphAuth, GraphClient
from dotenv import load_dotenv

def get_file_path() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="The path of the file to be downloaded.", type=str)
    args = parser.parse_args()
    return args.file_path

async def main(file_path: str) -> dict:
    BASE_URL = os.getenv("BASE_URL")
    if BASE_URL is None:
        raise RuntimeError("The BASE_URL environment variable has not been set.")
    broker = Broker()
    graph_client = GraphClient(base_url=BASE_URL, strategy=GraphAuth())
    tool = OnedriveReader(graph_client=graph_client)
    broker.register_tool(name=tool.name, tool=tool)
    arguments = {
        "file_path": file_path
    }
    file_content = await broker.dispatch(name="onedrive_reader", arguments=arguments)
    return file_content

if __name__ == "__main__":
    load_dotenv()
    file_content = asyncio.run(main(file_path=get_file_path()))
    print(file_content)


