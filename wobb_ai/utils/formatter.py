# utils/formatter.py
import re

class Formatter:
    @staticmethod
    def clean_and_format_output(data):
        """
        Cleans and formats the given data by:
        - Removing unwanted characters (\uf0fc, etc.)
        - Normalizing newlines
        - Adding ticks (✓) where applicable
        - Formatting as bullet points
        """
        # If data is a list, recursively clean each element
        if isinstance(data, list):
            return [Formatter.clean_and_format_output(item) for item in data]
        
        # If data is a string, clean it
        if isinstance(data, str):
            # Replace unwanted characters with ticks
            formatted_data = data.replace("\uf0fc", "✓")
            
            # Normalize newlines and trim spaces
            formatted_data = re.sub(r'\s*\n\s*', '\n', formatted_data.strip())
            
            # Split into bullet points for better readability
            if "\n" in formatted_data:
                formatted_data = "\n".join([f"• {line}" for line in formatted_data.split("\n")])
            
            return formatted_data
        
        # Return the original data if not a list or string
        return data