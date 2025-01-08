from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
#from langchain_ollama import OllamaLLM
from langchain_groq import ChatGroq
import json
import re

# Load environment variables
load_dotenv()

# Connect to the database
db = SQLDatabase.from_uri("mysql+mysqlconnector://root:password@localhost:3306/supply_chain_db")

def match_products_to_suppliers_chain(db):
    template = """
    You are a skilled SQL assistant specializing in crafting precise and optimized queries. Your task is to generate SQL queries based on the provided schemas and user questions.  

    **Schemas:**  
    - **Products Table:** {products}  
    - **Suppliers Table:** {suppliers}  

    **Instructions:**  
    1. Use only the above tables to generate valid SQL queries.  
    2. Provide **only the SQL query** and **JSON-formatted output**—no explanations or comments.  
    3. Return "none" in the Final Output if no results exist or if the query is invalid.  
    4. Calculate a compatibility score (0-10, 2 decimal places) for each product-supplier pair:  
        - The score reflects matching categories, MOQs, and location compatibility.  
        - Include this score in the final output for each product-supplier match.  
    5. Focus on precision and ensure the query is optimized for performance.  
    6. Do not generate fake data—use only database results.  

    Now answer: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0)
    #llm = OllamaLLM(model="llama3.2", temperature=0)
    
    return (
        RunnablePassthrough.assign(
            products=lambda _: db.get_table_info(table_names=["products"]),
            suppliers=lambda _: db.get_table_info(table_names=["suppliers"]),
        )
        | prompt
        | llm
        | StrOutputParser()
    )

def save_matches_chain():
    def save_to_db(matches):
        try:
            with db._engine.connect() as connection:
                for match in matches:
                    query = """
                    INSERT INTO product_supplier_matches (
                        product_name, supplier_name, product_category, supplier_category, location_match, compatibility_score
                    )
                    VALUES (
                        :product_name, :supplier_name, :product_category, :supplier_category, :location_match, :compatibility_score
                    );
                    """
                    connection.execute(
                        query,
                        product_name=match["Product Name"],
                        supplier_name=match["Supplier Name"],
                        product_category=match["Product Category"],
                        supplier_category=match["Supplier Category"],
                        location_match=match["Location Match"],
                        compatibility_score=match["Compatibility Score"]
                    )
            return "Matches saved to the database."
        except Exception as e:
            return f"Error saving matches: {str(e)}"

    return RunnablePassthrough(save_to_db)

if __name__ == "__main__":
    try:
        chain = match_products_to_suppliers_chain(db)

        # User input
        input_data = {
            "question": "Find suppliers for electronic components in California."
        }

        # Run the chain
        response = chain.invoke(input_data)
        print(response)

        # Extract JSON data
        response_json = json_data(response)
        print(response_json)

        # Save to the database
        save_chain = save_matches_chain()
        save_response = save_chain.invoke(response_json)
        print(save_response)

    except Exception as e:
        print(f"An error occurred: {e}")
