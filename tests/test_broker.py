import pytest, broker
from tools.base import Tool

class FakeTool(Tool):
    """A fake tool for use during unit testing."""
    @property
    def name(self) -> str:
        return "fake_tool"
    
    @property
    def description(self) -> str:
        return "This is just a test. If this were a real emergency you would be freaking out right now."
    
    @property
    def parameters(self) -> dict:
        return {
            "type": "test object",
            "properties": {
                "file path": {
                    "type": "string",
                    "description": "The fake path to the fake file."
                }
            },
            "required": ["file_path"]
        }
    
    async def execute(self, arguments: dict) -> dict:
        file_path = arguments["file_path"]
        output = {
            "file_path": file_path,
            "content": "This is test content. Yipeeeeee."
        }
        return output

@pytest.fixture
def test_broker():
    return broker.Broker()

class TestBroker():
    def test_register_tool(self, test_broker):
        name = "fake_tool_name"
        tool = FakeTool()
        tool2 = FakeTool()
        test_broker.register_tool(name=name, tool=tool)

        assert test_broker.registry[name] == tool

        test_broker.register_tool(name=name, tool=tool2)

        assert test_broker.registry[name] == tool

    @pytest.mark.asyncio
    async def test_dispatch(self, test_broker):
        name = "fake_tool_name"
        tool = FakeTool()
        test_broker.register_tool(name=name, tool=tool)

        arguments = {
            "file_path": "Z:/Fake/Path",
            "Distraction": "This should never be seen."
        }
        
        output = await test_broker.dispatch(name, arguments)
        assert output == {
            "file_path": "Z:/Fake/Path",
            "content": "This is test content. Yipeeeeee."
        }

        with pytest.raises(KeyError):
            output = await test_broker.dispatch(name="not_real", arguments=arguments)
