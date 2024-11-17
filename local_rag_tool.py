import re  # Import the re module for regular expressions
from nltk.tokenize import word_tokenize  # Import word_tokenize for tokenization
from nltk.corpus import stopwords  # Import stopwords for removing stop words

class LocalRAGTool:
    def __init__(self):
        pass  # No initialization required

    def extract_information(self, document_path, query):
        try:
            with open(document_path, 'r') as file:
                document_content = file.read()

            # 1. Tokenization and Stop Word Removal
            query_tokens = word_tokenize(query.lower())
            stop_words = set(stopwords.words('english'))
            query_tokens = [word for word in query_tokens if word not in stop_words]

            # 2. Search using Regular Expressions
            pattern = r"\b" + r"\b|\b".join(query_tokens) + r"\b"
            match = re.search(pattern, document_content.lower())

            if match:
                # 3. Extract Relevant Information (Example: Extract the sentence containing the match)
                sentence_start = document_content.lower().find(match.group(0))
                sentence_end = sentence_start + len(match.group(0))

                # Find the sentence boundaries (assuming sentences end with "." or "?")
                while sentence_end < len(document_content) and document_content[sentence_end] not in (".", "?"):
                    sentence_end += 1

                return document_content[sentence_start:sentence_end+1]

            else:
                return f"The query '{query}' was not found in the document."

        except FileNotFoundError:
            print(f"Error: File not found at '{document_path}'")
            return "Sorry, I couldn't find the file."

        except Exception as e:
            print(f"Error reading file: {e}")
            return "Sorry, there was an error reading the file."