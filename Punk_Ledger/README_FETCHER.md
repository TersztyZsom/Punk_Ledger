
# CryptoPunks Wallet Event Fetcher

This script fetches event data for specified wallet addresses related to CryptoPunks transactions. It connects to the Ethereum mainnet via Infura, processes event data from the CryptoPunks contract, and exports the data to an Excel file for further analysis.

## Good Quality Tuto vid here: https://youtu.be/sTiIBVmgTT8

## Features

- **Dynamic Wallet Address Input**: Users can input between 1 and 10 wallet addresses for querying.
- **Retry Logic for RPC Errors**: Handles errors by reducing block step size and retrying to avoid timeouts.
- **Event Fetching**: Fetches `PunkBought` events for the specified wallet addresses.
- **Excel Export**: Saves transaction data (Punk ID, wallet address, seller, buyer, price, and date) to an Excel file.

## Prerequisites

- Python 3.7 or higher
- The following Python libraries must be installed:
  - `web3`
  - `pandas`
  - `openpyxl`
- An Infura project API key
- An `abi.json` file containing the CryptoPunks contract ABI.

## Installation

1. Clone the repository or copy the script to your local environment.

2. Install the required dependencies using `pip`:

   ```bash
   pip install web3 pandas openpyxl
   ```

3. Obtain an Infura API key:
   - Create a free account at [Infura](https://infura.io/).
   - Create a new Ethereum project and note the API key.

4. Place the `abi.json` file (containing the CryptoPunks contract ABI) in the same directory as the script.

## Usage

1. Run the script:

   ```bash
   python script_name.py
   ```

2. **Wallet Addresses**: You will be prompted to enter between 1 and 10 valid Ethereum wallet addresses, separated by commas. Example:

   ```
   Enter wallet addresses separated by commas (1-10 addresses): 0x123..., 0x456..., 0x789...
   ```

   - Each wallet address must be valid (42 characters long, checksum format).

3. **Lowest Punk Price**: You will be prompted to enter the lowest CryptoPunk price in the following formats:

   - Examples: `35.99 ETH ($112,546.85 USD)` or `35.99 ETH $112,546.85 USD`

   The input helps confirm the latest price trend and is not used in querying.

4. **Fetching Events**: The script fetches `PunkBought` events for the specified wallets. It includes:

   - Punk ID
   - Wallet address
   - Role (Buyer or Seller)
   - Transaction hash
   - Seller and buyer addresses
   - Price (ETH)
   - Date

5. **Excel Export**: The collected data is saved in an Excel file named `wallet_transactions.xlsx`.

## Example Output

The output Excel file will contain the following columns:

| Punk ID | Wallet Address                        | Role   | Event  | Transaction Hash                                  | Seller                               | Buyer                                | Price (ETH) | Date                |
|---------|---------------------------------------|--------|--------|--------------------------------------------------|--------------------------------------|--------------------------------------|-------------|---------------------|
| 5664    | 0x0232d1083E970F0c78f56202b9A666B526F | Buyer  | Bought | 0x5c07e843fc852be94559d78e9170817841e5c8b4030e6 | 0x3935d398b67700508f0FEFba9006A2772 | 0x0232d1083E970F0c78f56202b9A666B52 | 54.69       | 2024-03-11 13:24:59 |

## Error Handling

- **RPC Errors**: The script retries queries when errors occur by reducing the block range dynamically.
- **Invalid Wallet Addresses**: Prompts the user to re-enter addresses if they are invalid.
- **Missing Event Data**: Skips events with missing data and logs errors in the console.

## Customization

### Modify Starting and Latest Block
You can adjust the block range by modifying these constants in the script:

```python
START_BLOCK = 0  # Adjust the starting block
LATEST_BLOCK = web3.eth.block_number  # Adjust the latest block if needed
```

### Adjust Block Step
The size of each query batch is controlled by:

```python
INITIAL_BLOCK_STEP = 1000000  # Change to increase/decrease batch size
MIN_BLOCK_STEP = 10000  # Minimum batch size for retries
```

## License

This project is open-source and can be freely modified and redistributed.

## Troubleshooting

- **Connection Issues**: Ensure that your internet connection is stable and that the Infura API key is valid.
- **Invalid ABI**: Verify that `abi.json` contains the correct CryptoPunks contract ABI.
- **No Events Found**: If no events are found, check that the wallet addresses provided have participated in CryptoPunks transactions.

---

Happy coding!
