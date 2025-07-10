# Mock globalVars module for jpDicTest.py
# This provides the minimal globalVars interface needed for testing
import os
import argparse


class MockAppArgs(argparse.Namespace):
	configPath = os.path.join(os.path.dirname(__file__), "..", "..", "source")


# Mock the essential globalVars attributes used by characterProcessing
appDir = os.path.join(os.path.dirname(__file__), "..", "..")
appArgs = MockAppArgs()
