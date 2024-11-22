
# CryptoPunks PnL Calculator

This script calculates the Profit and Loss (PnL) for a given CryptoPunk NFT based on wallet transactions. Users can specify their main wallet, additional linked wallets, Punk ID, and select specific timeframes for PnL calculations. It fetches transaction data from an Excel file and provides insights into CryptoPunk performance.

## Good Quality Tuto vid here: [https://youtu.be/sTiIBVmgTT8](https://youtu.be/UYcBKNzjeKw)

## Low Quality Tuto vid here:
https://github.com/user-attachments/assets/83403ced-3dab-4587-8b8a-de3b52f48384

## Features

- **Dynamic Wallet Input**: Users can specify a main wallet and additional linked wallets.
- **Timeframe-Based PnL Calculation**: Calculate PnL for multiple timeframes (e.g., 3 days, weekly, monthly, yearly).
- **Handles Unsold Punks**: Provides PnL e



stimates for unsold Punks based on the current lowest price.
- **Transaction Filtering**: Automatically filters and processes transaction data for a specific Punk ID and wallet.

## Prerequisites

- Python 3.7 or higher
- The following Python libraries must be installed:
  - `pandas`
- An Excel file named `wallet_transactions.xlsx` containing transaction data.

## Installation

1. Clone the repository or copy the script to your local environment.

2. Install the required dependencies using `pip`:

   ```bash
   pip install pandas
   ```

3. Ensure the `wallet_transactions.xlsx` file is in the same directory as the script.

## Usage

1. Run the script:

   ```bash
   python script_name.py
   ```

2. **Main Wallet Address**: Enter your main wallet address when prompted. Example:

   ```
   Enter the main Wallet Address (42 characters long): 0x1234...
   ```

   - Wallet addresses must be 42 characters long and start with "0x".

3. **Additional Wallets**: Choose whether to include additional linked wallets. If yes, enter them as a comma-separated list. Example:

   ```
   Enter linked wallet addresses separated by commas: 0x5678..., 0x9101...
   ```

4. **Punk ID**: Enter the numeric Punk ID for which you want to calculate PnL.

5. **Lowest Price**: Enter the current lowest price of the Punk in the following format:

   ```
   Enter the Current Lowest Price (e.g., '35.99 ETH ($112,683.97 USD)'): 35.99 ETH ($112,683.97 USD)
   ```

6. **Select Timeframes**: Choose one or more timeframes for PnL calculation:

   - 3 days
   - Weekly
   - Monthly
   - Yearly

   Example:

   ```
   Select the timeframes for PnL calculation (choose multiple by separating with commas):
   1. 3 days
   2. Weekly
   3. Monthly
   4. Yearly
   Enter your choices (e.g., 1,3): 1,2
   ```

7. **PnL Results**: The script calculates and displays the PnL for the specified timeframes.

## Example Output

### Console Output

```
📜 Transactions for the selected wallet and Punk ID:
           Date   Role   Event   Price (ETH)
2023-01-01  Buyer Bought  50
2023-01-15  Seller Sold   70

✅ Calculated PnL: Sale Price (70) - Purchase Price (50) = 20 ETH

📊 Final PnL Results by Timeframe:
  - 3-day PnL: No valid transaction within the timeframe
  - 7-day PnL: 20 ETH
  - Monthly PnL: 20 ETH
```

## Error Handling

- **Invalid Wallet Addresses**: Prompts the user to re-enter if the wallet address is invalid.
- **Missing Transactions**: Displays a warning and calculates PnL using the lowest price if no transactions are found.
- **File Not Found**: Prints an error message if `wallet_transactions.xlsx` is missing.

## Customization

### Modify Timeframes

To add or adjust timeframes for PnL calculation, edit the `calculate_time_period_pnl` function in the script.

## License

This project is open-source and can be freely modified and redistributed.

## Troubleshooting

- **Invalid Input**: Ensure wallet addresses are 42 characters long and Punk IDs are numeric.
- **Missing File**: Verify that `wallet_transactions.xlsx` exists in the working directory.
- **Empty Data**: Check that the Excel file contains valid transaction data.

---

Happy calculating!

