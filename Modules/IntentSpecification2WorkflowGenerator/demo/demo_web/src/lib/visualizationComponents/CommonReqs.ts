  export async function fetchCategoricalColumns(dataset: string): Promise<{ [key: string]: string }> {
    const response = await fetch("http://localhost:5000/dataset_categorical_columns", {
      method: "POST",
      body: JSON.stringify({ dataset }),
      headers: {
        "Content-Type": "application/json",
      },
    });
  
    if (!response.ok) {
      throw new Error('Failed to fetch categorical columns');
    }
  
    return response.json();
  }
  
  export async function fetchNumericalColumns(dataset: string): Promise<{ [key: string]: string }> {
    const response = await fetch("http://localhost:5000/dataset_numerical_columns", {
      method: "POST",
      body: JSON.stringify({ dataset }),
      headers: {
        "Content-Type": "application/json",
      },
    });
  
    if (!response.ok) {
      throw new Error('Failed to fetch numerical columns');
    }
  
    return response.json();
  }

  export async function fetchColumns(dataset: string): Promise<{ [key: string]: string }> {
    const response = await fetch("http://localhost:5000/dataset_columns", {
      method: "POST",
      body: JSON.stringify({ dataset }),
      headers: {
        "Content-Type": "application/json",
      },
    });
  
    if (!response.ok) {
      throw new Error('Failed to fetch columns');
    }
  
    return response.json();
  }
