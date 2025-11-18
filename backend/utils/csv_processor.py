import csv
import os

class CSVProcessor:
    """Process CSV files containing financial transactions"""
    
    def process_file(self, filepath):
        """
        Process a CSV file and return list of expenses
        
        Expected CSV format:
        date,category,amount,description
        2024-01-15,Food,85.50,Grocery Store
        """
        expenses = []
        
        if not os.path.exists(filepath):
            print(f"Error: File not found: {filepath}")
            return expenses
        
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                # Try to detect delimiter
                sample = file.read(1024)
                file.seek(0)
                
                # Use csv.Sniffer to detect format
                try:
                    delimiter = csv.Sniffer().sniff(sample).delimiter
                except:
                    delimiter = ','
                
                reader = csv.DictReader(file, delimiter=delimiter)
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        # Handle different possible column names
                        date = (row.get('date') or row.get('Date') or 
                               row.get('DATE') or '')
                        
                        category = (row.get('category') or row.get('Category') or 
                                   row.get('CATEGORY') or 'Other')
                        
                        amount_str = (row.get('amount') or row.get('Amount') or 
                                     row.get('AMOUNT') or '0')
                        
                        description = (row.get('description') or row.get('Description') or 
                                      row.get('DESCRIPTION') or row.get('name') or 
                                      row.get('Name') or '')
                        
                        # Clean and convert amount
                        amount_str = amount_str.replace('$', '').replace(',', '').strip()
                        amount = float(amount_str)
                        
                        expense = {
                            'date': date.strip(),
                            'category': category.strip(),
                            'amount': round(amount, 2),
                            'description': description.strip()
                        }
                        
                        expenses.append(expense)
                        
                    except ValueError as e:
                        print(f"Warning: Skipping row {row_num} - Invalid amount: {e}")
                        continue
                    except Exception as e:
                        print(f"Warning: Skipping row {row_num} - Error: {e}")
                        continue
                        
        except Exception as e:
            print(f"Error processing CSV file: {e}")
        
        print(f"Successfully processed {len(expenses)} expenses from CSV")
        return expenses