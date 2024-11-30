import unittest
from prompts.dynamic_prompts import DynamicPrompts

class TestDynamicPrompts(unittest.TestCase):
    def setUp(self):
        self.prompter = DynamicPrompts()

    def test_generate_prompt(self):
        document = "John works at Acme Corp."
        prompt = self.prompter.generate_prompt(document)
        self.assertIsInstance(prompt, str)
        self.assertTrue(len(prompt) > 0)