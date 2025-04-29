require('dotenv').config();
const { ethers } = require("ethers"); // Ensure correct import

// Your private key (Spirit Key)
const privateKey = process.env.PRIVATE_KEY;

// Connect to the Mumbai RPC
const provider = new ethers.JsonRpcProvider("https://rpc.ankr.com/polygon_mumbai");

// Create a wallet instance
const wallet = new ethers.Wallet(privateKey, provider);

// Define the SpiritCoin contract address and ABI
const contractAddress = "0x..."; // Your SpiritCoin contract address here
const abi = [
  // Add the ABI methods you need for minting
  "function mintBlessing(address to, uint256 amount, string memory blessingURI) public",
  // Add other methods from SpiritCoin contract as necessary
];

// Create a contract instance
const contract = new ethers.Contract(contractAddress, abi, wallet);

// Define the minting function
const mintBlessing = async (recipient, amount, uri) => {
  console.log(`Minting ${amount} SPIRIT for ${recipient}`);
  
  try {
    const tx = await contract.mintBlessing(recipient, amount, uri);
    await tx.wait();
    console.log(`Successfully minted ${amount} SPIRIT for ${recipient}`);
  } catch (error) {
    console.error("Error minting SPIRIT:", error);
  }
};

// Example Usage - Call this function when a trade happens or a spiritual milestone is reached
const exampleRecipient = "0x..."; // The recipient's address (wallet)
const exampleAmount = ethers.utils.parseUnits("10", 18); // Amount in SPIRIT (e.g., 10 SPIRIT)
const exampleURI = "ipfs://Qm..."; // IPFS URI (metadata for the blessing)

// Mint the blessing
mintBlessing(exampleRecipient, exampleAmount, exampleURI);
