import csv

class PersonalityService:
    def __init__(self, csv_path='data/persoai.csv'):
        self.csv_path = csv_path
        self.personalities = self.load_personalities()

    def load_personalities(self):
        """
        Load personality types, prompts, and tuning parameters from a CSV file.
        The CSV file should contain the following columns:
        - Personalidade: The name of the personality type.
        - Prompt: The specific prompt associated with this personality.
        - Tuning: The tuning parameters as a string (which will be converted to a dictionary).
        """
        personalities = {}
        try:
            with open(self.csv_path, 'r', encoding='ISO-8859-1') as file:  # Adjusted encoding to handle special characters
                reader = csv.DictReader(file)
                for row in reader:
                    personality_name = row['Personalidade'].strip()
                    prompt = row['Prompt'].strip()
                    tuning = row['Tuning'].strip()
                    # Convert tuning parameters from a string to a dictionary
                    tuning_dict = self.parse_tuning_parameters(tuning)
                    personalities[personality_name] = {
                        'prompt': prompt,
                        'tuning': tuning_dict
                    }
        except FileNotFoundError:
            print(f"The CSV file at {self.csv_path} was not found.")
        except KeyError as e:
            print(f"CSV file is missing required columns: {e}")
        except UnicodeDecodeError as e:
            print(f"Error reading the CSV file due to encoding: {e}")
        return personalities

    def parse_tuning_parameters(self, tuning_str):
        """
        Convert a tuning parameters string into a dictionary.
        The tuning string is expected to be in a comma-separated format like:
        'Alta confiança, baixa empatia, alta assertividade'
        """
        tuning_dict = {}
        for param in tuning_str.split(','):
            key_value = param.split('=')
            if len(key_value) == 2:
                key = key_value[0].strip().lower().replace(' ', '_')
                value = key_value[1].strip()
                tuning_dict[key] = value
            else:
                # In case the tuning is not in key=value format, we add it as a list item
                tuning_dict[f'param_{len(tuning_dict)+1}'] = param.strip()
        return tuning_dict

    def get_personality(self, personality_name):
        """
        Retrieve the prompt and tuning parameters for the given personality name.
        Returns 'neutral' if the personality name is not found.
        """
        return self.personalities.get(personality_name, {'prompt': 'neutral', 'tuning': {}})

    def list_personalities(self):
        """
        List all available personality types with their associated prompts and tuning parameters.
        """
        return self.personalities
