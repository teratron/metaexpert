//use config::*;
use std::env;
use std::error;

use sqlx::{Connection, postgres/*, Row*/};

mod config;

#[tokio::main]
async fn main() -> Result<(), Box<dyn error::Error>> {
    let _ = dotenv_vault::dotenv();

    // Binance
    let api_key = env::var("BINANCE_API_KEY").unwrap_or("ERR:".to_string());
    let api_secret = env::var("BINANCE_API_SECRET").unwrap_or("ERR:".to_string());
    println!("Key: {api_key}");
    println!("Secret: {api_secret}");

    // PostgreSQL
    let url = format!("postgresql://{user}:{password}@{host}:{port}/{name}",
                      user = env::var("DB_USER")
                          .unwrap_or("ERR: failed to get env with name 'DB_USER': {:?}".to_string()),
                      password = env::var("DB_PASSWORD")
                          .unwrap_or("ERR: failed to get env with name 'DB_PASSWORD': {:?}".to_string()),
                      host = env::var("DB_HOST")
                          .unwrap_or("ERR: failed to get env with name 'DB_HOST': {:?}".to_string()),
                      port = env::var("DB_PORT")
                          .unwrap_or("ERR: failed to get env with name 'DB_PORT': {:?}".to_string()),
                      name = env::var("DB_NAME")
                          .unwrap_or("ERR: failed to get env with name 'DB_NAME': {:?}".to_string()));

    println!("Connecting to {}", url);

    let mut conn = postgres::PgConnection::connect(&url).await?;
    let res = sqlx::query("SELECT t.* FROM prices t")
        .fetch_one(&mut conn)
        .await?;

    println!("{:?}", res);

    //let sum: i32 = res.get("sum");
    //println!("1 + 1 = {}", sum);

    Ok(())
}
