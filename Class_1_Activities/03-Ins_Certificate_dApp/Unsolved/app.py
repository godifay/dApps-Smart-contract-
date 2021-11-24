import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################

# Cache the contract on load

# Define the load_contract function

@st.cache(allow_output_mutation=True)
def load_contract():
    // TODO: Load the contract’s ABI details next

    # Load Art Gallery ABI
with open(Path('./contracts/compiled/artwork_abi.json')) as f:
    artwork_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
contract_address = os.getenv("SMART_CONTRACT_ADDRESS")    



    # Get the contract using web3
contract = w3.eth.contract(
    address=contract_address,
    abi=artwork_abi
)
return contract    



    # Return the contract from the function
@st.cache(allow_output_mutation=True)
def load_contract():
    with open(Path('./contracts/compiled/artwork_abi.json')) as f:
        artwork_abi = json.load(f)

    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    contract = w3.eth.contract(
        address=contract_address,
        abi=artwork_abi
    )

    return contract    



# Load the contract
contract = load_contract()
st.title("Register New Artwork")
accounts = w3.eth.accounts
address = st.selectbox("Select Artwork Owner", options=accounts)
artwork_uri = st.text_input("The URI to the artwork")

if st.button("Register Artwork"):
    tx_hash = contract.functions.registerArtwork(address, artwork_uri).transact({
        "from": address,
        "gas": 1000000
    })
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))


################################################################################
# Award Certificate
################################################################################

accounts = w3.eth.accounts
account = accounts[0]
student_account = st.selectbox("Select Account", options=accounts)
certificate_details = st.text_input("Certificate Details", value="FinTech Certificate of Completion")
if st.button("Award Certificate"):
    contract.functions.awardCertificate(student_account, certificate_details).transact({'from': account, 'gas': 1000000})

################################################################################
# Display Certificate
################################################################################
certificate_id = st.number_input("Enter a Certificate Token ID to display", value=0, step=1)
if st.button("Display Certificate"):
    # Get the certificate owner
    certificate_owner = contract.functions.ownerOf(certificate_id).call()
    st.write(f"The certificate was awarded to {certificate_owner}")

    # Get the certificate's metadata
    token_uri = contract.functions.tokenURI(certificate_id).call()
    st.write(f"The certificate's tokenURI metadata is {token_uri}")
