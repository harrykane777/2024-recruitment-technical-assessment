use axum::{http::StatusCode, response::IntoResponse, Json};
use serde::{Deserialize, Serialize};
use serde_json::Value;

pub async fn process_data(Json(request): Json<DataRequest>) -> impl IntoResponse {
    // Calculate sums and return response.
    let mut sum: i64 = 0;
    let mut length: usize = 0;

    // Process the numbers by adding to sum and the strings by adding
    // len to length.
    for value in request.data {
        match value {
            Value::Number(num) => {
                if let Some(n) = num.as_i64() {
                    sum += n
                }
            },
            Value::String(word) => {
                length += word.len()
            },
            _ => {}
        }
    }

    // Return response struct.
    let response = DataResponse {
        sum,
        length
    };

    (StatusCode::OK, Json(response))
}

#[derive(Deserialize)]
pub struct DataRequest {
    data: Vec<Value>
}

#[derive(Serialize)]
pub struct DataResponse {
    sum: i64, 
    length: usize
}
