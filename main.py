import argparse, os, asyncio
from broker import Broker
from tools.onedrive_pdf_reader import OnedrivePdfReader
from tools.onedrive_xlsx_reader import OnedriveXlsxReader
from tools.onedrive_docx_reader import OnedriveDocxReader
from graph.client import GraphAuth, GraphClient
from dotenv import load_dotenv

def get_file_path() -> list:
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", help="The name of the file to be downloaded.", type=str)
    parser.add_argument("upn", help="The user principal name of the user's Onedrive account.", type=str)
    args = parser.parse_args()
    inputs = [args.file_name, args.upn]
    return inputs

async def main(inputs: list) -> dict:
    BASE_URL = os.getenv("BASE_URL")
    if BASE_URL is None:
        raise RuntimeError("The BASE_URL environment variable has not been set.")
    broker = Broker()
    file_name = inputs[0]
    graph_client = GraphClient(base_url=BASE_URL, strategy=GraphAuth())
    if ".docx" in file_name:
        tool = OnedriveDocxReader(graph_client=graph_client)
    elif ".xlsx" in file_name:
        tool = OnedriveXlsxReader(graph_client=graph_client)
    elif ".pdf" in file_name:
        tool = OnedrivePdfReader(graph_client=graph_client)
    else:
        raise RuntimeError(f"The requested file {file_name} is not supported.")
    broker.register_tool(name=tool.name, tool=tool)
    arguments = {
        "file_name": file_name,
        "upn": inputs[1]
    }
    file_content = await broker.dispatch(name=tool.name, arguments=arguments)
    return file_content

if __name__ == "__main__":
    load_dotenv()
    file_content = asyncio.run(main(inputs=get_file_path()))
    print(file_content)


