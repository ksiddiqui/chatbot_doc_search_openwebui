# =============================================================================
# © 2025 Kashif Ali Siddiqui, Pakistan
# Developed by: Kashif Ali Siddiqui 
# Github: https://github.com/ksiddiqui
# LinkedIn: https://www.linkedin.com/in/ksiddiqui
# Email: kashif.ali.siddiqui@gmail.com
# Dated: July, 2025 
# -----------------------------------------------------------------------------
# This source code is the property of Kashif Ali Siddiqui and is confidential.
# Unauthorized copying or distribution of this file, via any medium, is strictly prohibited.
# =============================================================================

import json
import pandas as pd
import csv
import io
from typing import Optional

from roman import toRoman

markers = [
    {'name': 'json', 'start': '```json', 'end': '```'},
    {'name': 'markdown', 'start': '```', 'end': '```'},
    {'name': 'csv', 'start': '```csv', 'end': '```'},
    {'name': 'tsv', 'start': '```tsv', 'end': '```'},
    {'name': 'yaml', 'start': '```yaml', 'end': '```'},
    {'name': 'python', 'start': '```python', 'end': '```'},
    {'name': 'sql', 'start': '```sql', 'end': '```'},
    {'name': 'javascript', 'start': '```javascript', 'end': '```'},
    {'name': 'typescript', 'start': '```typescript', 'end': '```'},
    {'name': 'c', 'start': '```c', 'end': '```'},
    {'name': 'c++', 'start': '```c++', 'end': '```'},
    {'name': 'c#', 'start': '```c#', 'end': '```'},
    {'name': 'java', 'start': '```java', 'end': '```'},
    {'name': 'ruby', 'start': '```ruby', 'end': '```'},
    {'name': 'go', 'start': '```go', 'end': '```'},
    {'name': 'rust', 'start': '```rust', 'end': '```'},
    {'name': 'r', 'start': '```r', 'end': '```'},
    {'name': 'matlab', 'start': '```matlab', 'end': '```'},
    {'name': 'html', 'start': '```html', 'end': '```'},
    {'name': 'bash', 'start': '```bash', 'end': '```'},
    {'name': 'sh', 'start': '```sh', 'end': '```'},
]

def strip_markers(text: str, marker_type: str) -> str:
    marker_type = marker_type.lower() if marker_type else None
    if not marker_type or marker_type not in [m['name'] for m in markers]:
        return text
    
    text = text.strip()
    for marker in markers:
        if marker['name'] == marker_type:
            if text.startswith(marker['start']) and text.endswith(marker['end']):
                text = text[len(marker['start']):] # Remove start marker
                text = text[:-len(marker['end'])] # Remove end marker
                text = text.strip()
                break
    
    return text

def find_and_strip_markers(text: str, marker_type: str) -> str:
    marker_type = marker_type.lower() if marker_type else None
    if not marker_type:
        return text
    
    marker = next((m for m in markers if m['name'] == marker_type), None)
    if not marker:
        return text
    
    marker_start_seq = marker['start']
    marker_end_seq = marker['end']
    marker_start_seq_len = len(marker_start_seq)
    
    if marker_start_seq in text and marker_end_seq in text:
        start_idx = text.find(marker_start_seq)
        if start_idx != -1:
            end_idx = text.rfind(marker_end_seq)
            if end_idx > start_idx + marker_start_seq_len:
                text = text[start_idx + marker_start_seq_len:end_idx]
            else:
                text = text[start_idx + marker_start_seq_len:]
        text = text.strip()
    
    return text

def convert_to_json(response_text: str, force_find_json=False) -> dict:

    if force_find_json:
        # Find first and last of { and }, and get the string inbetween including markers
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}')
        response_text = response_text[start_idx:end_idx+1]
    else:
        response_text = find_and_strip_markers(response_text, 'json')

    response_json = None
    try:
        response_json = json.loads(response_text)
    except json.JSONDecodeError as e:
        error_message = f"Exception type {type(e).__name__} occurred while parsing JSON: {str(e)}"
        print(error_message)
        print(response_text)
        print("===")
        # No UI error handling here as this is a utility function
            
    return response_json

def convert_to_dataframe(csv_text: str, headers: list[str] = None) -> Optional[pd.DataFrame]:
    
    csv_text = find_and_strip_markers(csv_text, 'csv')
    
    try:
        csv_buffer = io.StringIO(csv_text)
        if headers:
            # First check if the CSV has headers by reading the first line
            csv_buffer.seek(0)
            has_header = csv.Sniffer().has_header(csv_buffer.read(1024))
            csv_buffer.seek(0)
            
            if has_header:
                # If CSV has headers, skip the first row (original headers)
                df = pd.read_csv(csv_buffer, quoting=csv.QUOTE_ALL, skipinitialspace=True, header=0)
                # Replace the original headers with the provided ones
                df.columns = headers
            else:
                # If CSV doesn't have headers, just use the provided headers
                df = pd.read_csv(csv_buffer, quoting=csv.QUOTE_ALL, skipinitialspace=True, header=None)
                df.columns = headers
        else:
            # If no headers provided, use the CSV's headers if they exist
            df = pd.read_csv(csv_buffer, quoting=csv.QUOTE_ALL, skipinitialspace=True)
        
        return df
    except Exception as e:
        error_message = f"Exception type {type(e).__name__} occurred while parsing CSV. Details: {str(e)}"
        print(error_message)
        print(csv_text)
        print("===")
    return None #pd.DataFrame()

    
def generate_excel(data_list: list, output_file_path: str, sheet_names: Optional[list] = None):
    with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
        for idx, data in enumerate(data_list):
            df = pd.DataFrame(data)
            sheet_name = sheet_names[idx] if sheet_names and idx < len(sheet_names) else f"Sheet{idx+1}"
            
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    return output_file_path


def read_text_file_without_comments(file_path: str, ignore_comments: bool = True, comment_symbol: str = '#', encoding: str = 'utf-8') -> str:
    with open(file_path, 'r', encoding=encoding) as file:
        lines = file.readlines()
    
    if ignore_comments:
        lines = [line for line in lines if not line.strip().startswith(comment_symbol)]
    
    return ''.join(lines)

def get_value_from_json(json_data: dict, key_path: list[str], default_value = None):
    if not json_data or not key_path or len(key_path) == 0:
        return None
    
    current_data = json_data
    for key in key_path:
        if isinstance(current_data, dict) and key in current_data:
            current_data = current_data[key]
        else:
            return default_value
    
    return current_data
    
def format_json_as_tree(data, indent=0, dict_bullet="•", list_bullet="–", numbered_lists=True, add_extra_newline=False):
    result = ""
    prefix = "  " * indent
    extra_line = '\n' if add_extra_newline else ''
    
    def format_recursive_call(item, current_indent, is_list_item=False):
        return format_json_as_tree(item, current_indent, dict_bullet=dict_bullet, list_bullet=list_bullet, numbered_lists=numbered_lists, add_extra_newline=add_extra_newline)
    
    def get_item_prefix(index=None):
        if index is not None:
            return f"{index}." if numbered_lists else list_bullet
        return dict_bullet

    if isinstance(data, dict):
        for key, value in data.items():
            title = key.replace("_", " ").title()
            
            if isinstance(value, dict):
                result += f"{prefix}{dict_bullet} {title}:\n{extra_line}"
                result += format_recursive_call(value, indent + 2)
            
            elif isinstance(value, list):
                result += f"{prefix}{dict_bullet} {title}:\n{extra_line}"
                for i, item in enumerate(value, 1):
                    item_prefix = get_item_prefix(i)
                    if isinstance(item, (dict, list)):
                        result += f"{prefix}  {item_prefix} \n"
                        result += format_recursive_call(item, indent + 2)
                    else:
                        result += f"{prefix}  {item_prefix} {item}\n{extra_line}"
            
            else:
                result += f"{prefix}{dict_bullet} {title}: {value}\n"

    elif isinstance(data, list):
        for i, item in enumerate(data, 1):
            item_prefix = get_item_prefix(i)
            if isinstance(item, (dict, list)):
                result += f"{prefix}{item_prefix} \n"
                result += format_recursive_call(item, indent + 2, True)
            else:
                result += f"{prefix}{item_prefix} {item}\n{extra_line}"

    else:
        result += f"{prefix}{dict_bullet} {data}\n{extra_line}"
    return result

def render_json_for_markdown(data, initial_indent=0):
    output = []
    
    def _get_formatted_key_and_prefix(key, current_item_index, level_index):
        formatted_key = key.replace("_", " ").title()
        item_prefix = ""
        if level_index == 0:
            item_prefix = f"{current_item_index + 1}. "
        elif level_index == 1:
            item_prefix = f"{chr(97 + current_item_index)}. "
        elif level_index == 2:
            item_prefix = f"{toRoman(current_item_index + 1)}. "
        return formatted_key, item_prefix
    
    def _get_list_item_prefix(current_item_index, level_index):
        item_prefix = ""
        if level_index == 0:
            item_prefix = f"{current_item_index + 1}. "
        elif level_index == 1:
            item_prefix = f"{chr(97 + current_item_index)}. "
        elif level_index == 2:
            item_prefix = f"{toRoman(current_item_index + 1)}. "
        return item_prefix
    
    def _render(current_data, indent, level_index):
        current_indent_str = '  ' * indent
        current_item_index = 0

        if isinstance(current_data, dict):
            if level_index < 3:
                for key, value in current_data.items():
                    formatted_key, item_prefix = _get_formatted_key_and_prefix(key, current_item_index, level_index)                    
                    if isinstance(value, (dict, list)):
                        output.append(f"{current_indent_str}{item_prefix}**{formatted_key}**:\n")
                        _render(value, indent + 1, level_index + 1)
                    else:
                        output.append(f"{current_indent_str}{item_prefix}**{formatted_key}**: {value}\n")
                    current_item_index += 1
            else:
                for key, value in current_data.items():
                    formatted_key, _ = _get_formatted_key_and_prefix(key, 0, level_index) # i is not used for bullet points
                    if isinstance(value, (dict, list)):
                        output.append(f"{current_indent_str}* **{formatted_key}**:")
                        _render(value, indent + 1, level_index + 1)
                    else:
                        output.append(f"{current_indent_str}* **{formatted_key}**: {value}")

        elif isinstance(current_data, list):
            if level_index < 3:
                for value in current_data:
                    item_prefix = _get_list_item_prefix(current_item_index, level_index)

                    if isinstance(value, (dict, list)):
                        output.append(f"{current_indent_str}{item_prefix}")
                        _render(value, indent + 1, level_index + 1)
                    else:
                        output.append(f"{current_indent_str}{item_prefix}{value}")
                    current_item_index += 1
            else:
                for value in current_data:
                    if isinstance(value, (dict, list)):
                        output.append(f"{current_indent_str}* ")
                        _render(value, indent + 1, level_index + 1)
                    else:
                        output.append(f"{current_indent_str}* {value}")
        else:
            output.append(f"{current_indent_str}{current_data}")

    _render(data, initial_indent, 0)
    return "\n".join(output)


class DictTreeFormatter:
    def __init__(self, numbered_levels=3):
        self.numbered_levels = numbered_levels

    def format(self, data: dict) -> str:
        return self._render_tree(data)

    def _render_tree(self, data, level=0, index_stack=None):
        if index_stack is None:
            index_stack = []

        lines = []
        indent = '    ' * level

        if isinstance(data, dict):
            for i, (key, value) in enumerate(data.items(), 1):
                bullet = self._get_bullet(level, i)
                prefix = f"{indent}{bullet} {self._format_key(key)}"

                if isinstance(value, (dict, list)):
                    lines.append(prefix)
                    lines.append(self._render_tree(value, level + 1, index_stack + [i]))
                else:
                    lines.append(f"{prefix}: {value}")

        elif isinstance(data, list):
            for i, item in enumerate(data, 1):
                bullet = self._get_bullet(level, i)
                prefix = f"{indent}{bullet}"
                if isinstance(item, (dict, list)):
                    lines.append(prefix)
                    lines.append(self._render_tree(item, level + 1, index_stack + [i]))
                else:
                    lines.append(f"{prefix} {item}")

        else:
            lines.append(f"{indent}{data}")

        return '\n'.join(lines)

    def _format_key(self, key: str) -> str:
        return f"**{key.replace('_', ' ').title()}**"

    def _get_bullet(self, level: int, index: int) -> str:
        if level == 0:
            return f"{index}."
        elif level == 1:
            return f"{chr(96 + index)}."
        elif level == 2:
            return f"{self._int_to_roman(index)}."
        else:
            return "-"

    def _int_to_roman(self, n: int) -> str:
        romans = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x',
                  'xi', 'xii', 'xiii', 'xiv', 'xv', 'xvi', 'xvii', 'xviii', 'xix', 'xx',
                  'xxi', 'xxii', 'xxiii', 'xxiv', 'xxv', 'xxvi', 'xxvii', 'xxviii', 'xxix', 'xxx',
                  'xxxi', 'xxxii', 'xxxiii', 'xxxiv', 'xxxv', 'xxxvi', 'xxxvii', 'xxxviii', 'xxxix', 'xl']
        return romans[n - 1] if 1 <= n <= len(romans) else str(n)


def format_list_as_string(data_list:list, single_line:bool = False) -> str:
    if single_line:
        # Comma separated list on single line
        return ", ".join([f"{item}" for item in data_list if item])
    
    # Bullet point list on multiple lines
    return "\n".join([f"- {item}" for item in data_list if item])