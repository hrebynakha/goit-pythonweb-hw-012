import argparse
import asyncio
import asyncpg
import ssl


async def create_db(user, password, host, dbname):
    ssl_context = ssl.create_default_context(cafile="rds-ca-bundle.pem")  # default CA

    conn = await asyncpg.connect(
        user=user,
        password=password,
        host=host,
        database="postgres",  # default DB
        ssl=ssl_context,
    )
    exists = await conn.fetchval("SELECT 1 FROM pg_database WHERE datname = $1", dbname)
    if not exists:
        await conn.execute(f'CREATE DATABASE "{dbname}"')
        print(f"Database {dbname} created.")
    else:
        print(f"Database {dbname} already exists.")
    await conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create Postgres database if it does not exist"
    )
    parser.add_argument("--username", required=True, help="DB username")
    parser.add_argument("--password", required=True, help="DB password")
    parser.add_argument("--host", required=True, help="DB host")
    parser.add_argument("--dbname", required=True, help="Database name to create")

    args = parser.parse_args()

    asyncio.run(create_db(args.username, args.password, args.host, args.dbname))
