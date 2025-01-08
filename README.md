# Product-Supplier Matching Application

This application automates the process of matching products to suppliers based on defined compatibility criteria, such as categories, minimum order quantities (MOQs), and location. It uses a combination of SQL queries, a language model for generating precise queries, and a database to store results.

## Features

- **Dynamic Query Generation**: Generates SQL queries dynamically based on user-provided questions.
- **Compatibility Scoring**: Computes a compatibility score (0-10) for product-supplier pairs.
- **Database Integration**: Saves matching results into a database table for future reference.
- **JSON Parsing**: Extracts and formats results in JSON format.
- **Extensible Framework**: Adaptable for different use cases like freelancer-job matching, customer-product matching, etc.

---

## Requirements

### **Dependencies**
The following Python libraries are required:
- `dotenv`: To manage environment variables.
- `langchain_core`: For prompt templates and runnable pipelines.
- `langchain_community`: To interact with SQL databases.
- `langchain_groq`: For utilizing the ChatGroq model.
- `json`: For JSON parsing.
- `re`: For regular expressions.

### **Database**
- A MySQL database configured with the following tables:
  - `products`: Stores product details.
  - `suppliers`: Stores supplier details.
  - `product_supplier_matches`: Stores matching results.

---

## Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Configure the `.env` file:
    ```
    DATABASE_URL=mysql+mysqlconnector://<username>:<password>@<host>:<port>/<database_name>
    ```

4. Ensure the database schema matches the required structure.

---

## How to Run

1. **Run the Script**:
    ```bash
    python main.py
    ```

2. **Provide Input Questions**:
   Modify the `input_data` dictionary in the script with your specific query, e.g.,
   ```python
   input_data = {
       "question": "Find suppliers for electronic components in California."
   }
   ```

3. **View Output**:
   - JSON results will be printed in the console.
   - Matching results are saved in the `product_supplier_matches` table.

---

## File Structure

- `main.py`: The main script to run the application.
- `requirements.txt`: Lists all required Python libraries.
- `.env`: Environment configuration file.
- `README.md`: Documentation for the project.

---

## Workflow Overview

1. **Query Generation**:
   - The user provides a question (e.g., "Find suppliers for electronics").
   - The language model generates an optimized SQL query using the provided schema.

2. **Data Retrieval**:
   - The query retrieves product and supplier data from the database.

3. **Compatibility Scoring**:
   - Compatibility is calculated based on matching categories, MOQs, and location.

4. **Results Formatting**:
   - The results are returned in JSON format and saved to the database.

---

## Use Cases

1. **Product-Supplier Matching**: Match products to suppliers based on compatibility criteria.
2. **Freelancer-Job Matching**: Adapt to match freelancers to job postings.
3. **Customer-Product Matching**: Find products that best match customer preferences.

---

## Example Output

### Input Question
```json
{
  "question": "Find suppliers for electronic components in California."
}
```

### SQL Query Generated
```sql
SELECT p.product_name, s.supplier_name, p.category AS product_category, s.category AS supplier_category,
       (CASE WHEN p.location = s.location THEN 10 ELSE 5 END) AS location_match,
       ROUND((CHAR_LENGTH(REPLACE(LOWER(s.category), LOWER(p.category), '')) / CHAR_LENGTH(s.category)) * 10, 2) AS compatibility_score
FROM products p
JOIN suppliers s ON p.category LIKE CONCAT('%', s.category, '%');
```

### Final Output
```json
[
  {
    "Product Name": "Resistor",
    "Supplier Name": "Electro Supply Co.",
    "Product Category": "Electronics",
    "Supplier Category": "Electronic Components",
    "Location Match": 10,
    "Compatibility Score": 9.5
  }
]
```

---

## Contributors

- **Ibrahim Toheeb**: Developer and maintainer.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

- **LangChain**: For providing a robust framework for building AI-powered pipelines.
- **OpenAI**: For inspiring modern AI integrations.
- **Groq Models**: For enabling advanced language model capabilities.

