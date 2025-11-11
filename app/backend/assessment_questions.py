"""Comprehensive assessment questions for all modules (170 total)"""
from typing import List
from app.backend.models.assessment import Assessment, QuestionType


def get_module_1_assessments() -> List[Assessment]:
    """Module 1: Blockchain Technology - 10 multiple-choice questions"""
    return [
        Assessment(
            module_id=1,
            question_text="What is a distributed ledger?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            order_index=1,
            points=10,
            options={
                "A": "A centralized database managed by a single authority",
                "B": "A shared database that is synchronized across multiple locations",
                "C": "A cloud storage service",
                "D": "A type of spreadsheet"
            },
            correct_answer="B",
            explanation="A distributed ledger is a shared database that is synchronized across multiple locations, participants, or institutions. Unlike a centralized database, no single party controls it.",
            is_active=True,
        ),
        Assessment(
            module_id=1,
            question_text="What is the primary purpose of a blockchain?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            order_index=2,
            points=10,
            options={
                "A": "To store large amounts of data",
                "B": "To create an immutable record of transactions",
                "C": "To speed up internet connections",
                "D": "To replace traditional databases"
            },
            correct_answer="B",
            explanation="The primary purpose of a blockchain is to create an immutable, tamper-proof record of transactions that can be verified by all participants.",
            is_active=True,
        ),
        Assessment(
            module_id=1,
            question_text="What is a block in a blockchain?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            order_index=3,
            points=10,
            options={
                "A": "A physical storage device",
                "B": "A collection of transactions grouped together and cryptographically linked to the previous block",
                "C": "A type of cryptocurrency",
                "D": "A network node"
            },
            correct_answer="B",
            explanation="A block is a collection of transactions that are grouped together and cryptographically linked to the previous block, forming a chain.",
            is_active=True,
        ),
        Assessment(
            module_id=1,
            question_text="What does 'immutable' mean in the context of blockchain?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            order_index=4,
            points=10,
            options={
                "A": "Can be easily changed",
                "B": "Cannot be altered or deleted once recorded",
                "C": "Requires permission to view",
                "D": "Stored in multiple locations"
            },
            correct_answer="B",
            explanation="Immutable means that once data is recorded on the blockchain, it cannot be altered or deleted. This is a key security feature of blockchain technology.",
            is_active=True,
        ),
        Assessment(
            module_id=1,
            question_text="Does blockchain require a central authority to validate transactions?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            order_index=5,
            points=10,
            options={
                "A": "Yes, all blockchains require a central authority",
                "B": "No, blockchain is decentralized and uses consensus mechanisms",
                "C": "Only private blockchains require central authority",
                "D": "It depends on the type of data being stored"
            },
            correct_answer="B",
            explanation="Blockchain is decentralized and does not require a central authority. Transactions are validated by network participants through consensus mechanisms like Proof-of-Work or Proof-of-Stake.",
            is_active=True,
        ),
        Assessment(
            module_id=1,
            question_text="Can a block be easily modified once it's added to the blockchain?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            order_index=6,
            points=10,
            options={
                "A": "Yes, blocks can be edited at any time",
                "B": "No, blocks are cryptographically linked making modification extremely difficult",
                "C": "Only the most recent block can be modified",
                "D": "Blocks can be modified with special permission"
            },
            correct_answer="B",
            explanation="Blocks are cryptographically linked, making it extremely difficult to modify past blocks without invalidating the entire chain. This immutability is a core security feature.",
            is_active=True,
        ),
        Assessment(
            module_id=1,
            question_text="What makes blockchain technology secure?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            order_index=7,
            points=10,
            options={
                "A": "Only authorized users can access it",
                "B": "Cryptographic hashing, distributed consensus, and immutability",
                "C": "It's stored on a single secure server",
                "D": "It requires passwords to view"
            },
            correct_answer="B",
            explanation="Blockchain security comes from multiple factors: cryptographic hashing links blocks together, distributed consensus ensures agreement, and immutability prevents tampering.",
            is_active=True,
        ),
        Assessment(
            module_id=1,
            question_text="What is a real-world application of blockchain technology besides cryptocurrency?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            order_index=8,
            points=10,
            options={
                "A": "Blockchain can only be used for cryptocurrencies",
                "B": "Supply chain tracking, digital identity, voting systems, and medical records",
                "C": "Only financial transactions",
                "D": "Only data storage"
            },
            correct_answer="B",
            explanation="Blockchain has many applications beyond cryptocurrencies, including supply chain management, digital identity verification, secure voting systems, medical record keeping, and more.",
            is_active=True,
        ),
        Assessment(
            module_id=1,
            question_text="How are blocks connected in a blockchain?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            order_index=9,
            points=10,
            options={
                "A": "Blocks are stored in the same physical location",
                "B": "Each block contains a hash of the previous block, creating a cryptographic chain",
                "C": "Blocks are connected by network cables",
                "D": "Blocks are linked by user permissions"
            },
            correct_answer="B",
            explanation="Blocks are connected cryptographically - each block contains a hash (digital fingerprint) of the previous block, creating an unbreakable chain. Any modification to a block would change its hash and break the chain.",
            is_active=True,
        ),
        Assessment(
            module_id=1,
            question_text="What is the main difference between a blockchain and a traditional database?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            order_index=10,
            points=10,
            options={
                "A": "There is no difference",
                "B": "Blockchain is decentralized and immutable, while traditional databases are centralized and can be modified",
                "C": "Blockchain is faster than traditional databases",
                "D": "Traditional databases are more secure"
            },
            correct_answer="B",
            explanation="The key differences are: blockchain is decentralized (no single point of control) and immutable (data cannot be easily changed), while traditional databases are typically centralized and allow modifications.",
            is_active=True,
        ),
    ]


def get_all_assessments() -> dict[int, List[Assessment]]:
    """Returns a dictionary mapping module_id to list of Assessment objects"""
    assessments = {}
    
    # All modules including Module 1
    assessments[1] = get_module_1_assessments()
    assessments[2] = get_module_2_assessments()
    assessments[3] = get_module_3_assessments()
    assessments[4] = get_module_4_assessments()
    assessments[5] = get_module_5_assessments()
    assessments[6] = get_module_6_assessments()
    assessments[7] = get_module_7_assessments()
    assessments[8] = get_module_8_assessments()
    assessments[9] = get_module_9_assessments()
    assessments[10] = get_module_10_assessments()
    assessments[11] = get_module_11_assessments()
    assessments[12] = get_module_12_assessments()
    assessments[13] = get_module_13_assessments()
    assessments[14] = get_module_14_assessments()
    assessments[15] = get_module_15_assessments()
    assessments[16] = get_module_16_assessments()
    assessments[17] = get_module_17_assessments()
    
    return assessments


def get_module_2_assessments() -> List[Assessment]:
    """Module 2: Web3 Wallets & Security - 10 multiple-choice questions"""
    return [
        Assessment(module_id=2, question_text="What is the relationship between a public key and private key?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=1, points=10,
            options={"A": "Public key is your password, private key is your address", "B": "Public key is your address (shareable), private key is your password (secret)", "C": "They are the same thing", "D": "Public key is secret, private key is public"},
            correct_answer="B", explanation="The public key is your blockchain address that you can share with others. The private key is the secret code that proves ownership and must never be shared.", is_active=True),
        Assessment(module_id=2, question_text="What is the main difference between a custodial and non-custodial wallet?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=2, points=10,
            options={"A": "Custodial wallets are free, non-custodial cost money", "B": "Custodial: third party holds your keys; Non-custodial: you control your keys", "C": "Custodial wallets are more secure", "D": "There is no difference"},
            correct_answer="B", explanation="Custodial wallets are managed by a third party (like an exchange) who holds your private keys. Non-custodial wallets give you full control of your private keys.", is_active=True),
        Assessment(module_id=2, question_text="What is a seed phrase (recovery phrase)?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=3, points=10,
            options={"A": "A password for your wallet", "B": "A list of words that can restore your entire wallet and all private keys", "C": "Your public address", "D": "A type of cryptocurrency"},
            correct_answer="B", explanation="A seed phrase is a list of words (typically 12 or 24) that can restore your entire wallet. It's the master key to all your private keys.", is_active=True),
        Assessment(module_id=2, question_text="Which type of wallet is generally considered more secure for storing large amounts?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=4, points=10,
            options={"A": "Hot wallet (software)", "B": "Cold wallet (hardware)", "C": "Custodial wallet", "D": "Browser extension wallet"},
            correct_answer="B", explanation="Cold wallets (hardware wallets) are considered more secure because private keys never leave the device and are not connected to the internet.", is_active=True),
        Assessment(module_id=2, question_text="How should you store your seed phrase to keep it safe?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=5, points=10,
            options={"A": "Take a screenshot or photo and save it to the cloud", "B": "Write it down and store copies in secure offline locations", "C": "Email it to yourself so you can search for it later", "D": "Memorize it and destroy any physical copy"},
            correct_answer="B", explanation="Seed phrases should be written down and stored securely offline. Digital copies can be compromised if your device or cloud storage is hacked.", is_active=True),
        Assessment(module_id=2, question_text="What does the phrase 'Not your keys, not your coins' warn about?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=6, points=10,
            options={"A": "Hardware wallets are the only secure option", "B": "Exchanges always protect customer funds", "C": "If you don't control the private keys, you don't truly own the assets", "D": "Seed phrases are optional for non-custodial wallets"},
            correct_answer="C", explanation="If a third party controls the private keys, they ultimately control the funds. True ownership requires holding your own private keys.", is_active=True),
        Assessment(module_id=2, question_text="If you lose your private key but still have your seed phrase, what can you do?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=7, points=10,
            options={"A": "Nothing—the wallet is lost forever", "B": "Use the seed phrase to regenerate the wallet and private keys", "C": "Ask the blockchain to reset your password", "D": "Contact a miner to unlock the funds"},
            correct_answer="B", explanation="Your seed phrase can regenerate all private keys, allowing you to recover the wallet even if the original private key is lost.", is_active=True),
        Assessment(module_id=2, question_text="Why must you never share your private key or seed phrase?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=8, points=10,
            options={"A": "Sharing it slows down your wallet", "B": "Anyone with it can take complete control of your assets", "C": "It voids any hardware wallet warranty", "D": "It prevents you from staking tokens"},
            correct_answer="B", explanation="Private keys and seed phrases grant full control of your assets. Sharing them lets others transfer or steal your funds with no way to reverse the loss.", is_active=True),
        Assessment(module_id=2, question_text="How do hot wallets differ from cold wallets?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=9, points=10,
            options={"A": "Hot wallets are only for NFTs, cold wallets only for coins", "B": "Hot wallets stay connected to the internet; cold wallets remain offline", "C": "Hot wallets are physical devices; cold wallets are browser extensions", "D": "Hot wallets can never be used for DeFi"},
            correct_answer="B", explanation="Hot wallets are internet-connected and convenient for daily transactions. Cold wallets remain offline to minimize exposure to online attacks.", is_active=True),
        Assessment(module_id=2, question_text="Which precaution best protects you from common Web3 scams?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=10, points=10,
            options={"A": "Signing every transaction request to be helpful", "B": "Only interacting with smart contracts that have no audits", "C": "Double-checking URLs and contract addresses before approving actions", "D": "Sharing your seed phrase with customer support"},
            correct_answer="C", explanation="Phishing and malicious contracts are common. Always verify URLs, contract addresses, and transaction requests before approving them.", is_active=True),
    ]


def get_module_3_assessments() -> List[Assessment]:
    """Module 3: Transactions, dApps & Gas Fees - 10 questions"""
    return [
        Assessment(module_id=3, question_text="What are the four main components of a blockchain transaction?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=1, points=10,
            options={"A": "From, To, Amount, Data", "B": "Sender, Receiver, Value, Time", "C": "Address, Key, Balance, Hash", "D": "Block, Chain, Hash, Nonce"},
            correct_answer="A", explanation="A transaction contains: From (sender address), To (receiver address), Amount (value being transferred), and Data (optional additional information).", is_active=True),
        Assessment(module_id=3, question_text="What is the mempool?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=2, points=10,
            options={"A": "A type of cryptocurrency", "B": "A pool where transactions wait to be processed and added to a block", "C": "A wallet address", "D": "A smart contract"},
            correct_answer="B", explanation="The mempool (memory pool) is where pending transactions wait before being included in a block by miners/validators.", is_active=True),
        Assessment(module_id=3, question_text="What are gas fees?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=3, points=10,
            options={"A": "Fees for using electricity", "B": "Fees paid to validators/miners to process transactions on the blockchain", "C": "Fees for storing data", "D": "Fees for creating wallets"},
            correct_answer="B", explanation="Gas fees are payments made to network validators or miners to process and validate transactions on the blockchain.", is_active=True),
        Assessment(module_id=3, question_text="What is a dApp (decentralized application)?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=4, points=10,
            options={"A": "An app that runs on your phone", "B": "An application that runs on the blockchain using smart contracts", "C": "A traditional web application", "D": "A type of wallet"},
            correct_answer="B", explanation="A dApp is a decentralized application that runs on a blockchain, typically using smart contracts for its backend logic.", is_active=True),
        Assessment(module_id=3, question_text="Which statement best describes gas fees on a public blockchain?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=5, points=10,
            options={"A": "Gas fees are fixed and never change", "B": "Gas fees fluctuate based on network activity and transaction demand", "C": "Gas fees only apply to token transfers", "D": "Gas fees are paid directly to wallet providers"},
            correct_answer="B", explanation="Gas fees are market-driven. When demand for block space rises, users bid higher fees to prioritize their transactions.", is_active=True),
        Assessment(module_id=3, question_text="How do Layer-2 solutions affect transaction costs and speed?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=6, points=10,
            options={"A": "They increase fees but slow transactions", "B": "They remove the need for validators entirely", "C": "They process transactions off-chain to reduce congestion and fees", "D": "They are only used for NFTs, not payments"},
            correct_answer="C", explanation="Layer-2 networks batch or process transactions off the main chain, then settle to Layer-1, reducing congestion and lowering fees for users.", is_active=True),
        Assessment(module_id=3, question_text="Why do most dApps ask you to connect a wallet before you can use them?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=7, points=10,
            options={"A": "To send promotional emails", "B": "To access your private keys directly", "C": "To read on-chain data tied to your address and request transaction signatures", "D": "To store your password for you"},
            correct_answer="C", explanation="Connecting a wallet lets the dApp read your address, check token balances, and request transaction signatures when you interact with smart contracts.", is_active=True),
        Assessment(module_id=3, question_text="Which factors have the greatest impact on the gas fee you ultimately pay?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=8, points=10,
            options={"A": "Hash rate of Bitcoin miners", "B": "Network congestion, gas price you set, and the complexity of the transaction", "C": "The color scheme of the dApp", "D": "The age of your wallet"},
            correct_answer="B", explanation="Gas cost is influenced by how busy the network is, the base fee, the priority fee (tip) you set, and how computationally intensive the transaction is.", is_active=True),
        Assessment(module_id=3, question_text="What is the primary goal of Layer-2 scaling solutions?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=9, points=10,
            options={"A": "To replace Layer-1 blockchains entirely", "B": "To add more tokens to the ecosystem", "C": "To improve throughput and reduce fees without sacrificing security", "D": "To eliminate smart contracts"},
            correct_answer="C", explanation="Layer-2 solutions aim to scale transaction capacity and lower fees while still inheriting the security guarantees of the underlying Layer-1 blockchain.", is_active=True),
        Assessment(module_id=3, question_text="How does a decentralized application (dApp) differ from a traditional application?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=10, points=10,
            options={"A": "dApps only work offline", "B": "dApps rely on smart contracts on a blockchain instead of a centralized server", "C": "Traditional apps cannot have user interfaces", "D": "dApps are always free to use"},
            correct_answer="B", explanation="dApps use smart contracts deployed on a blockchain for backend logic, while traditional applications rely on centralized servers controlled by an organization.", is_active=True),
    ]


def get_module_4_assessments() -> List[Assessment]:
    """Module 4: Tokens & Digital Assets - 10 questions"""
    return [
        Assessment(module_id=4, question_text="What is the difference between a coin and a token?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=1, points=10,
            options={"A": "There is no difference", "B": "Coins are native to a blockchain (like BTC, ETH), tokens are built on top of a blockchain", "C": "Coins are more valuable", "D": "Tokens are only NFTs"},
            correct_answer="B", explanation="Coins are the native cryptocurrency of a blockchain (Bitcoin on Bitcoin, Ether on Ethereum). Tokens are created on top of existing blockchains using smart contracts.", is_active=True),
        Assessment(module_id=4, question_text="What is tokenomics?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=2, points=10,
            options={"A": "The study of token prices", "B": "The economics of a token including supply, demand, minting, and burning", "C": "A type of token", "D": "Token trading strategies"},
            correct_answer="B", explanation="Tokenomics refers to the economic model of a token, including its supply mechanisms, distribution, utility, and how it creates value.", is_active=True),
        Assessment(module_id=4, question_text="What is an ERC-20 token?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=3, points=10,
            options={"A": "A type of NFT", "B": "A fungible token standard on Ethereum", "C": "A blockchain", "D": "A wallet type"},
            correct_answer="B", explanation="ERC-20 is a standard for fungible (interchangeable) tokens on Ethereum. Most tokens like USDC, DAI follow this standard.", is_active=True),
        Assessment(module_id=4, question_text="What is an NFT (Non-Fungible Token)?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=4, points=10,
            options={"A": "A type of cryptocurrency", "B": "A unique, non-interchangeable token that represents ownership of a digital or physical asset", "C": "A fungible token", "D": "A smart contract"},
            correct_answer="B", explanation="An NFT is a unique token that represents ownership of a specific item. Each NFT is distinct and cannot be replaced by another.", is_active=True),
        Assessment(module_id=4, question_text="When you purchase an NFT, what do you actually own?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=5, points=10,
            options={"A": "The underlying artwork file stored anywhere on the internet", "B": "A blockchain token that references the asset and proves ownership", "C": "Exclusive copyright to the artwork in every case", "D": "All assets created by the original artist"},
            correct_answer="B", explanation="An NFT is a token recorded on-chain that points to metadata describing the asset. Ownership of the token does not automatically transfer copyright unless explicitly stated.", is_active=True),
        Assessment(module_id=4, question_text="What is the primary characteristic of a fiat-backed stablecoin?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=6, points=10,
            options={"A": "Its value floats freely with market demand", "B": "It is pegged to another asset like USD and backed by reserves", "C": "It only exists on private blockchains", "D": "It cannot be redeemed for fiat currency"},
            correct_answer="B", explanation="Stablecoins such as USDC maintain a 1:1 peg to a fiat currency and are typically backed by reserve assets to reduce volatility.", is_active=True),
        Assessment(module_id=4, question_text="Which statement about Ethereum token standards is accurate?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=7, points=10,
            options={"A": "All Ethereum tokens follow the ERC-20 standard", "B": "ERC-721 is used for non-fungible tokens and ERC-1155 can support multiple token types", "C": "ERC-20 is only used for NFTs", "D": "Ethereum has no formal token standards"},
            correct_answer="B", explanation="Ethereum supports multiple standards: ERC-20 for fungible tokens, ERC-721 for NFTs, and ERC-1155 for mixed fungible/non-fungible assets.", is_active=True),
        Assessment(module_id=4, question_text="How do utility tokens differ from governance tokens?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=8, points=10,
            options={"A": "Utility tokens provide platform access; governance tokens grant voting rights", "B": "Utility tokens are always stablecoins", "C": "Governance tokens are only used on centralized exchanges", "D": "There is no difference between them"},
            correct_answer="A", explanation="Utility tokens unlock services or features within an ecosystem, while governance tokens allow holders to vote on proposals and protocol changes.", is_active=True),
        Assessment(module_id=4, question_text="What is token burning designed to accomplish?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=9, points=10,
            options={"A": "Increase the number of tokens in circulation", "B": "Permanently remove tokens to reduce supply and create scarcity", "C": "Reset the token's smart contract", "D": "Freeze user wallets to prevent fraud"},
            correct_answer="B", explanation="Burning tokens removes them from circulation, often as a deflationary mechanism intended to support long-term value.", is_active=True),
        Assessment(module_id=4, question_text="Why is metadata critical for NFTs?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=10, points=10,
            options={"A": "Metadata stores the smart contract code", "B": "Metadata describes the NFT's content, attributes, and links to media files", "C": "Metadata determines gas prices", "D": "Metadata controls the NFT's resale price"},
            correct_answer="B", explanation="NFT metadata contains information such as the asset's name, description, image link, and traits, helping wallets and marketplaces display the NFT accurately.", is_active=True),
    ]


def get_module_5_assessments() -> List[Assessment]:
    """Module 5: Trading - 10 questions"""
    return [
        Assessment(module_id=5, question_text="What is a CEX (Centralized Exchange)?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=1, points=10,
            options={"A": "A decentralized exchange", "B": "A private company that operates a trading platform (like Coinbase, Binance)", "C": "A type of wallet", "D": "A smart contract"},
            correct_answer="B", explanation="A CEX is a centralized exchange run by a company that acts as an intermediary for trading cryptocurrencies.", is_active=True),
        Assessment(module_id=5, question_text="What is a DEX (Decentralized Exchange)?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=2, points=10,
            options={"A": "A company-run exchange", "B": "A smart contract-based exchange that allows peer-to-peer trading without intermediaries", "C": "A type of token", "D": "A blockchain"},
            correct_answer="B", explanation="A DEX uses smart contracts to enable direct peer-to-peer trading without a central authority holding funds.", is_active=True),
        Assessment(module_id=5, question_text="What is the difference between a market order and a limit order?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=3, points=10,
            options={"A": "Market order executes immediately at current price; Limit order executes only at your specified price", "B": "They are the same", "C": "Market orders are cheaper", "D": "Limit orders are faster"},
            correct_answer="A", explanation="Market orders buy/sell immediately at the best available price. Limit orders only execute when the price reaches your specified level.", is_active=True),
        Assessment(module_id=5, question_text="What does 'FOMO' mean in trading?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=4, points=10,
            options={"A": "Fear of Missing Out - making emotional decisions based on fear of missing gains", "B": "A type of order", "C": "A trading strategy", "D": "A cryptocurrency"},
            correct_answer="A", explanation="FOMO (Fear of Missing Out) leads traders to make impulsive decisions based on emotions rather than analysis, often resulting in poor timing.", is_active=True),
        Assessment(module_id=5, question_text="What is a key characteristic of most decentralized exchanges (DEXs)?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=5, points=10,
            options={"A": "They always require government-issued IDs for KYC", "B": "They let users trade directly from their wallets without surrendering custody", "C": "They only support fiat trading pairs", "D": "They are run by a single company"},
            correct_answer="B", explanation="DEXs are non-custodial platforms where smart contracts facilitate trades directly between users, so KYC is typically not required.", is_active=True),
        Assessment(module_id=5, question_text="Why do newcomers often start on centralized exchanges (CEXs)?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=6, points=10,
            options={"A": "CEXs have no fees and no custodial risk", "B": "CEXs provide simple interfaces, fiat on-ramps, and customer support", "C": "CEXs do not require account creation", "D": "CEXs only list reputable tokens"},
            correct_answer="B", explanation="Centralized exchanges streamline the user experience with easy onboarding, fiat gateways, and support, making them approachable for beginners.", is_active=True),
        Assessment(module_id=5, question_text="Which guideline reflects responsible crypto investing?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=7, points=10,
            options={"A": "Borrow as much as possible to maximize gains", "B": "Only invest funds you can afford to lose", "C": "Focus on one token and never diversify", "D": "Invest immediately whenever prices spike"},
            correct_answer="B", explanation="Crypto markets are volatile. Limiting exposure to money you can afford to lose helps manage downside risk.", is_active=True),
        Assessment(module_id=5, question_text="What is a trade-off between using a CEX versus a DEX?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=8, points=10,
            options={"A": "CEXs allow self-custody; DEXs take custody", "B": "CEXs are centralized with faster execution; DEXs are non-custodial but may require more technical knowledge", "C": "CEXs only support stablecoins; DEXs support fiat", "D": "There are no differences between the two"},
            correct_answer="B", explanation="CEXs provide speed and convenience but require trusting a custodian. DEXs preserve self-custody at the cost of higher learning curve and potential gas fees.", is_active=True),
        Assessment(module_id=5, question_text="Why is risk management essential for traders?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=9, points=10,
            options={"A": "It guarantees profits on every trade", "B": "It sets rules for position size, stop losses, and portfolio balance to limit downside", "C": "It removes the need to monitor the market", "D": "It lets you ignore diversification"},
            correct_answer="B", explanation="Risk management strategies such as position sizing, stop losses, and diversification protect capital when trades go against you.", is_active=True),
        Assessment(module_id=5, question_text="What does 'impermanent loss' describe for liquidity providers?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=10, points=10,
            options={"A": "Permanent loss caused by hacked smart contracts", "B": "Loss that only occurs if you provide liquidity for less than 24 hours", "C": "The temporary value difference between holding tokens separately versus in a liquidity pool", "D": "A penalty charged by exchanges for withdrawing liquidity"},
            correct_answer="C", explanation="Impermanent loss occurs when the relative prices of tokens in a liquidity pool change, causing the pooled value to differ from simply holding the tokens.", is_active=True),
    ]


def get_module_6_assessments() -> List[Assessment]:
    """Module 6: DeFi & DAOs - 10 questions"""
    return [
        Assessment(module_id=6, question_text="What does DeFi stand for?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=1, points=10,
            options={"A": "Decentralized Finance", "B": "Digital Finance", "C": "Defined Finance", "D": "Direct Finance"},
            correct_answer="A", explanation="DeFi stands for Decentralized Finance - financial services built on blockchain without traditional intermediaries.", is_active=True),
        Assessment(module_id=6, question_text="What is a liquidity pool?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=2, points=10,
            options={"A": "A type of wallet", "B": "A pool of two tokens locked in a smart contract that enables trading", "C": "A cryptocurrency", "D": "A blockchain"},
            correct_answer="B", explanation="A liquidity pool is a collection of two tokens locked in a smart contract that allows users to swap between them.", is_active=True),
        Assessment(module_id=6, question_text="What is yield farming?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=3, points=10,
            options={"A": "Growing crops on a farm", "B": "Providing liquidity to DeFi protocols to earn rewards or interest", "C": "Trading tokens", "D": "Mining cryptocurrency"},
            correct_answer="B", explanation="Yield farming involves providing liquidity to DeFi protocols in exchange for rewards, typically in the form of tokens or interest.", is_active=True),
        Assessment(module_id=6, question_text="What is a DAO?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=4, points=10,
            options={"A": "A type of token", "B": "Decentralized Autonomous Organization - an internet-native organization run by code and community governance", "C": "A cryptocurrency exchange", "D": "A smart contract"},
            correct_answer="B", explanation="A DAO is a Decentralized Autonomous Organization governed by smart contracts and community voting, without traditional hierarchical management.", is_active=True),
        Assessment(module_id=6, question_text="How do most DeFi lending platforms manage borrower risk?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=5, points=10,
            options={"A": "They require no collateral for any loan", "B": "They rely on credit scores issued by banks", "C": "They require borrowers to deposit crypto collateral worth more than the loan", "D": "They insure every loan through governments"},
            correct_answer="C", explanation="DeFi lending platforms typically require over-collateralization, locking more value than the amount borrowed to protect lenders.", is_active=True),
        Assessment(module_id=6, question_text="How do DAO governance tokens typically function?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=6, points=10,
            options={"A": "They provide staking rewards only", "B": "They allow holders to vote on proposals and treasury decisions", "C": "They automatically guarantee price appreciation", "D": "They replace smart contracts entirely"},
            correct_answer="B", explanation="Governance tokens give community members voting power to influence protocol changes, budgets, and strategic decisions.", is_active=True),
        Assessment(module_id=6, question_text="What causes impermanent loss for liquidity providers?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=7, points=10,
            options={"A": "Only downward price movement for both assets", "B": "Price fluctuations between the pooled assets compared to simply holding them", "C": "Protocol fees collected from traders", "D": "Smart contract fees charged by miners"},
            correct_answer="B", explanation="Impermanent loss occurs when the relative price of assets in a pool changes, altering the value of a provider's share versus holding the assets outright.", is_active=True),
        Assessment(module_id=6, question_text="How does DeFi lending differ from borrowing at a traditional bank?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=8, points=10,
            options={"A": "DeFi lending requires in-person paperwork", "B": "DeFi lending uses smart contracts, global access, and over-collateralized loans without credit checks", "C": "Traditional banks are fully automated like DeFi", "D": "DeFi loans always have lower interest rates"},
            correct_answer="B", explanation="DeFi lending is permissionless, automated via smart contracts, global, and typically requires over-collateralization rather than credit scores.", is_active=True),
        Assessment(module_id=6, question_text="Which risk should DeFi participants carefully monitor?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=9, points=10,
            options={"A": "Smart contract vulnerabilities and protocol hacks", "B": "Government-backed deposit insurance", "C": "Guaranteed returns from liquidity pools", "D": "Traditional bank overdraft fees"},
            correct_answer="A", explanation="Smart contract bugs, oracle manipulation, and protocol exploits remain key risks for DeFi users.", is_active=True),
        Assessment(module_id=6, question_text="How are decisions typically executed within a DAO?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=10, points=10,
            options={"A": "A CEO approves all decisions manually", "B": "Token holders vote on proposals and smart contracts enforce approved actions", "C": "Decisions are mailed to members for approval", "D": "Only venture capital investors can vote"},
            correct_answer="B", explanation="DAO members submit proposals, token holders vote, and smart contracts execute approved outcomes, ensuring transparent on-chain governance.", is_active=True),
    ]


def get_module_7_assessments() -> List[Assessment]:
    """Module 7: Advanced Concepts Overview - 10 questions"""
    return [
        Assessment(module_id=7, question_text="What is pseudonymity in blockchain?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=1, points=10,
            options={"A": "Complete anonymity", "B": "Transactions are linked to addresses, not real identities, but can be traced", "C": "Transactions are completely private", "D": "A type of cryptocurrency"},
            correct_answer="B", explanation="Blockchains are pseudonymous - addresses aren't directly tied to identities, but all transactions are public and traceable.", is_active=True),
        Assessment(module_id=7, question_text="What is a Zero-Knowledge Proof (ZKP)?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=2, points=10,
            options={"A": "A type of blockchain", "B": "A way to prove something is true without revealing the underlying information", "C": "A cryptocurrency", "D": "A wallet"},
            correct_answer="B", explanation="Zero-Knowledge Proofs allow you to prove you know something (like a password) without revealing what it is.", is_active=True),
        Assessment(module_id=7, question_text="What is a blockchain bridge?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=3, points=10,
            options={"A": "A physical structure", "B": "A protocol that allows transferring assets between different blockchains", "C": "A type of wallet", "D": "A smart contract"},
            correct_answer="B", explanation="Bridges enable interoperability between blockchains, allowing you to move assets from one chain to another.", is_active=True),
        Assessment(module_id=7, question_text="What is a wrapped token (e.g., WBTC)?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=4, points=10,
            options={"A": "A damaged token", "B": "A token that represents another blockchain's native asset on a different chain", "C": "A type of NFT", "D": "A token standard"},
            correct_answer="B", explanation="Wrapped tokens represent assets from one blockchain on another. WBTC is Bitcoin wrapped to work on Ethereum.", is_active=True),
        Assessment(module_id=7, question_text="Which statement best describes on-chain privacy?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=5, points=10,
            options={"A": "All transactions on public blockchains are fully anonymous", "B": "Addresses are pseudonymous, but transactions remain visible and traceable", "C": "Transactions are hidden by default", "D": "Users must register their real identities on-chain"},
            correct_answer="B", explanation="Public blockchains record every transaction. Addresses are pseudonymous, but flows can be analyzed to infer identity.", is_active=True),
        Assessment(module_id=7, question_text="How do mixing services impact transaction privacy?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=6, points=10,
            options={"A": "They destroy funds permanently", "B": "They combine funds from multiple users to obscure the transaction trail", "C": "They freeze coins indefinitely", "D": "They prevent users from ever withdrawing"},
            correct_answer="B", explanation="Mixers pool and redistribute funds to make it harder to trace ownership, though they carry regulatory and compliance concerns.", is_active=True),
        Assessment(module_id=7, question_text="Why are blockchain bridges needed for interoperability?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=7, points=10,
            options={"A": "Blockchains natively share state without bridges", "B": "Bridges convert proof-of-work chains to proof-of-stake", "C": "Independent blockchains cannot communicate directly, so bridges transfer assets or data between them", "D": "Bridges only create new wallets"},
            correct_answer="C", explanation="Each blockchain maintains its own state. Bridges lock tokens on one chain and mint representations on another to enable cross-chain movement.", is_active=True),
        Assessment(module_id=7, question_text="Which tool can enhance user privacy on public blockchains?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=8, points=10,
            options={"A": "Zero-knowledge proofs and privacy-focused wallets", "B": "Disabling encryption", "C": "Posting private keys on forums", "D": "Reducing block sizes"},
            correct_answer="A", explanation="Zero-knowledge proofs, mixers, and privacy coins help conceal transaction details while maintaining network integrity.", is_active=True),
        Assessment(module_id=7, question_text="What is a major challenge with cross-chain interoperability?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=9, points=10,
            options={"A": "All blockchains use identical consensus mechanisms", "B": "Different chains have unique security models and require trusted or trust-minimized bridges", "C": "No blockchain supports smart contracts", "D": "Users cannot hold tokens on more than one chain"},
            correct_answer="B", explanation="Each chain has distinct security assumptions. Bridges must account for differing consensus rules, trust requirements, and potential attack vectors.", is_active=True),
        Assessment(module_id=7, question_text="How do ASIC miners differ from GPU miners in proof-of-work networks?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=10, points=10,
            options={"A": "ASICs are general-purpose while GPUs are specialized", "B": "ASICs are specialized hardware for one algorithm, offering higher efficiency than general-purpose GPUs", "C": "GPUs consume less power for the same hash rate as ASICs", "D": "Only GPUs can mine Bitcoin"},
            correct_answer="B", explanation="ASICs are purpose-built for a specific algorithm, delivering superior hash rates and efficiency compared to multi-purpose GPUs.", is_active=True),
    ]


def get_module_8_assessments() -> List[Assessment]:
    """Module 8: Practical On-Chain Analysis - 10 questions"""
    return [
        Assessment(module_id=8, question_text="What is a block explorer?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=1, points=10,
            options={"A": "A type of wallet", "B": "A search engine and web interface for viewing blockchain data", "C": "A cryptocurrency", "D": "A smart contract"},
            correct_answer="B", explanation="A block explorer is a tool that allows you to search and view all publicly available data on a blockchain, like transactions, addresses, and blocks.", is_active=True),
        Assessment(module_id=8, question_text="What can you do in the 'Read Contract' tab on a block explorer?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=2, points=10,
            options={"A": "Execute transactions", "B": "Query public data from a contract without spending gas", "C": "Modify contract code", "D": "Delete contracts"},
            correct_answer="B", explanation="The Read Contract tab lets you view public data from smart contracts for free without connecting a wallet or paying gas.", is_active=True),
        Assessment(module_id=8, question_text="What is wallet tracing?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=3, points=10,
            options={"A": "Following a wallet's transaction history to understand its activity", "B": "Stealing from a wallet", "C": "Creating a new wallet", "D": "A type of transaction"},
            correct_answer="A", explanation="Wallet tracing involves following a wallet's complete transaction history to understand where funds came from and where they went.", is_active=True),
        Assessment(module_id=8, question_text="What is TVL (Total Value Locked)?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=4, points=10,
            options={"A": "A type of token", "B": "The total value of assets locked in a DeFi protocol", "C": "A wallet balance", "D": "Transaction volume"},
            correct_answer="B", explanation="TVL measures the total value of cryptocurrency locked in a DeFi protocol, indicating its size and popularity.", is_active=True),
        Assessment(module_id=8, question_text="Who typically operates public block explorers such as Etherscan?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=5, points=10,
            options={"A": "The blockchain protocol itself", "B": "Independent third-party companies that index blockchain data", "C": "Only government agencies", "D": "Individual wallet owners"},
            correct_answer="B", explanation="Block explorers are generally maintained by independent organizations that index raw blockchain data and provide searchable interfaces.", is_active=True),
        Assessment(module_id=8, question_text="Do you need to connect a wallet to read smart contract data on a block explorer?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=6, points=10,
            options={"A": "Yes, otherwise the data is hidden", "B": "Only if the contract is on a testnet", "C": "No, the read functions are public and free to query", "D": "Only if the contract owner grants permission"},
            correct_answer="C", explanation="Read Contract functions expose public state variables, allowing anyone to query data without signing a transaction or connecting a wallet.", is_active=True),
        Assessment(module_id=8, question_text="What level of transparency do public blockchains provide for transactions?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=7, points=10,
            options={"A": "Transactions are private and hidden by default", "B": "Only account balances are visible", "C": "Every transaction is recorded publicly and can be viewed on explorers", "D": "Only miners can see transaction data"},
            correct_answer="C", explanation="Public blockchains maintain an open ledger where transaction details are visible to anyone using tools like block explorers.", is_active=True),
        Assessment(module_id=8, question_text="How can you verify a pending transaction using a block explorer?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=8, points=10,
            options={"A": "By calling customer service", "B": "By searching the transaction hash to view status, sender, receiver, and gas details", "C": "By refreshing your wallet repeatedly", "D": "By exporting the private key"},
            correct_answer="B", explanation="Entering the transaction hash on an explorer reveals whether it's pending or confirmed, along with addresses and amounts involved.", is_active=True),
        Assessment(module_id=8, question_text="What insight does Total Value Locked (TVL) provide about a DeFi protocol?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=9, points=10,
            options={"A": "The protocol's gas fee schedule", "B": "How many developers contribute code", "C": "The amount of capital users have deposited, indicating usage and trust", "D": "The number of NFTs minted"},
            correct_answer="C", explanation="TVL reflects how much capital is deployed in a protocol, helping gauge its adoption, liquidity, and perceived safety.", is_active=True),
        Assessment(module_id=8, question_text="How could you investigate a suspicious wallet address?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=10, points=10,
            options={"A": "By asking the wallet owner for details", "B": "By reviewing its transaction history, tracing inflows/outflows, and checking interactions with known addresses", "C": "By deleting the address from the blockchain", "D": "By recreating the wallet locally"},
            correct_answer="B", explanation="Analyzing transaction flows, counterparties, and interactions with known exchanges or flagged addresses helps identify potential scams.", is_active=True),
    ]


def get_module_9_assessments() -> List[Assessment]:
    """Module 9: Advanced Market & Tokenomic Analysis - 10 questions"""
    return [
        Assessment(module_id=9, question_text="What is Technical Analysis (TA)?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=1, points=10,
            options={"A": "Analyzing code", "B": "Analyzing price charts and patterns to predict future price movements", "C": "Analyzing wallets", "D": "Analyzing smart contracts"},
            correct_answer="B", explanation="Technical Analysis involves studying price charts, patterns, and indicators to make trading decisions.", is_active=True),
        Assessment(module_id=9, question_text="What is Fundamental Analysis (FA) in crypto?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=2, points=10,
            options={"A": "Only looking at price", "B": "Evaluating a project's team, technology, tokenomics, and community to assess value", "C": "Chart patterns", "D": "Trading volume only"},
            correct_answer="B", explanation="Fundamental Analysis evaluates the intrinsic value of a project by examining its fundamentals like team, tech, tokenomics, and adoption.", is_active=True),
        Assessment(module_id=9, question_text="What does RSI (Relative Strength Index) measure?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=3, points=10,
            options={"A": "Transaction speed", "B": "Whether an asset is overbought or oversold", "C": "Wallet balance", "D": "Gas fees"},
            correct_answer="B", explanation="RSI is a momentum indicator that measures whether an asset is overbought (above 70) or oversold (below 30).", is_active=True),
        Assessment(module_id=9, question_text="What are on-chain metrics?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=4, points=10,
            options={"A": "Price charts", "B": "Data derived from blockchain activity like active addresses, hash rate, transaction volume", "C": "Trading indicators", "D": "Wallet types"},
            correct_answer="B", explanation="On-chain metrics analyze blockchain data such as active addresses, transaction counts, and network activity to gauge market sentiment.", is_active=True),
        Assessment(module_id=9, question_text="What is a limitation of Technical Analysis (TA)?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=5, points=10,
            options={"A": "TA guarantees future price movements", "B": "TA provides probabilistic insights but cannot predict with certainty", "C": "TA ignores historical price data", "D": "TA only applies to stocks"},
            correct_answer="B", explanation="TA helps form probability-based scenarios using historical data, but market outcomes remain uncertain.", is_active=True),
        Assessment(module_id=9, question_text="Which activity is a core part of Fundamental Analysis?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=6, points=10,
            options={"A": "Ignoring project documentation", "B": "Reviewing the whitepaper, roadmap, and team background", "C": "Only studying candlestick patterns", "D": "Tracking the RSI indicator"},
            correct_answer="B", explanation="Fundamental analysts evaluate project documentation, tokenomics, team quality, and competitive landscape to assess value.", is_active=True),
        Assessment(module_id=9, question_text="How should high on-chain activity be interpreted?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=7, points=10,
            options={"A": "It always signals a bullish market", "B": "It must be combined with context—activity could indicate adoption or increased sell pressure", "C": "It has no relevance for analysis", "D": "It only occurs on proof-of-stake chains"},
            correct_answer="B", explanation="Elevated activity could signify rising adoption, but it might also reflect redemptions or sell-offs; analysts must consider context.", is_active=True),
        Assessment(module_id=9, question_text="What do support and resistance levels represent?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=8, points=10,
            options={"A": "Random price points with no trader interest", "B": "Zones where buying or selling pressure historically emerges", "C": "Guarantees that price will stop moving", "D": "Only psychological levels in fiat markets"},
            correct_answer="B", explanation="Support often marks demand zones where buyers step in, while resistance reflects supply zones where sellers emerge.", is_active=True),
        Assessment(module_id=9, question_text="Which factors are important when assessing a project's tokenomics?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=9, points=10,
            options={"A": "Only the logo design", "B": "Total supply, distribution, vesting schedules, and utility", "C": "Community memes", "D": "The number of social media followers alone"},
            correct_answer="B", explanation="Robust tokenomics analysis examines supply, emission schedules, allocation, and utility to understand incentives and potential dilution.", is_active=True),
        Assessment(module_id=9, question_text="How can on-chain metrics inform investment decisions?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=10, points=10,
            options={"A": "They are irrelevant for public blockchains", "B": "They reveal wallet behavior, accumulation trends, and network growth", "C": "They only show historical prices", "D": "They replace the need for any other research"},
            correct_answer="B", explanation="On-chain data helps identify trends such as whale accumulation, user adoption, and liquidity flows, complementing other forms of analysis.", is_active=True),
    ]


def get_module_10_assessments() -> List[Assessment]:
    """Module 10: Advanced DeFi Strategies - 10 questions"""
    return [
        Assessment(module_id=10, question_text="What is leveraged yield farming?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=1, points=10,
            options={"A": "Farming without leverage", "B": "Using borrowed funds to amplify yield farming returns (and risks)", "C": "A type of token", "D": "A wallet"},
            correct_answer="B", explanation="Leveraged yield farming involves borrowing additional capital to increase position size and potential returns, but also amplifies risks.", is_active=True),
        Assessment(module_id=10, question_text="What is a delta-neutral strategy?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=2, points=10,
            options={"A": "A strategy that profits regardless of price direction by hedging", "B": "A strategy that only works when price goes up", "C": "A type of token", "D": "A trading pair"},
            correct_answer="A", explanation="Delta-neutral strategies use hedging to profit from other factors (like fees, funding rates) while minimizing exposure to price movements.", is_active=True),
        Assessment(module_id=10, question_text="What are DeFi derivatives?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=3, points=10,
            options={"A": "Basic tokens", "B": "Financial instruments (perpetuals, options, synthetics) built on DeFi protocols", "C": "Wallets", "D": "Blockchains"},
            correct_answer="B", explanation="DeFi derivatives are advanced financial products like perpetuals, options, and synthetic assets built on decentralized protocols.", is_active=True),
        Assessment(module_id=10, question_text="What is protocol risk in DeFi?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=4, points=10,
            options={"A": "Risk of price going down", "B": "Risk of smart contract bugs, economic attacks, or protocol failures", "C": "Risk of losing your wallet", "D": "Risk of high gas fees"},
            correct_answer="B", explanation="Protocol risk includes smart contract vulnerabilities, economic exploits, oracle failures, and other risks inherent to the protocol itself.", is_active=True),
        Assessment(module_id=10, question_text="How does leverage impact potential trading outcomes?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=5, points=10,
            options={"A": "It always guarantees higher profits", "B": "It increases both potential gains and potential losses", "C": "It eliminates liquidation risk", "D": "It removes the need for collateral"},
            correct_answer="B", explanation="Leverage magnifies price exposure, so profitable moves yield larger gains but adverse moves can trigger liquidations quickly.", is_active=True),
        Assessment(module_id=10, question_text="What is a realistic expectation for delta-neutral strategies?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=6, points=10,
            options={"A": "They remove every type of risk", "B": "They hedge price exposure but still face funding, execution, and protocol risks", "C": "They only work in bull markets", "D": "They require no active management"},
            correct_answer="B", explanation="Delta-neutral strategies hedge directional risk but remain exposed to factors like funding rates, liquidity, and smart contract risk.", is_active=True),
        Assessment(module_id=10, question_text="How do DeFi protocols differ in risk profiles?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=7, points=10,
            options={"A": "All protocols share the same audited code", "B": "Risk varies based on audits, design, team, and liquidity safeguards", "C": "Only new protocols are risky", "D": "Protocol risk is irrelevant if APY is high"},
            correct_answer="B", explanation="Each protocol has unique code quality, economic design, and safeguards; due diligence is vital to understand associated risks.", is_active=True),
        Assessment(module_id=10, question_text="What is oracle risk and why does it matter?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=8, points=10,
            options={"A": "Risk that users forget their passwords", "B": "Dependence on external data feeds that can be manipulated or fail", "C": "Risk that block times speed up", "D": "Only a concern for centralized exchanges"},
            correct_answer="B", explanation="DeFi protocols rely on oracles for external prices. Manipulated or failing oracles can lead to incorrect liquidations or protocol insolvency.", is_active=True),
        Assessment(module_id=10, question_text="What factors should be reviewed when evaluating protocol risk?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=9, points=10,
            options={"A": "Only the headline APY", "B": "Audits, bug bounties, TVL, team reputation, and insurance coverage", "C": "The number of memes in Discord", "D": "Whether the protocol has a mobile app"},
            correct_answer="B", explanation="Risk assessment looks at code audits, security incentives, liquidity depth, team history, insurance, and governance structure.", is_active=True),
        Assessment(module_id=10, question_text="What is a key trade-off in leveraged yield farming strategies?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=10, points=10,
            options={"A": "Lower yields with lower risk", "B": "Higher potential returns at the cost of liquidation risk, funding costs, and increased complexity", "C": "Guaranteed profits with minimal effort", "D": "No need to monitor positions"},
            correct_answer="B", explanation="Leverage can boost yields but introduces risks like liquidation, higher borrowing costs, and exposure to smart contract failures.", is_active=True),
    ]


def get_module_11_assessments() -> List[Assessment]:
    """Module 11: Development & Programming Prerequisites - 10 questions"""
    return [
        Assessment(module_id=11, question_text="What is a variable in programming?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=1, points=10,
            options={"A": "A fixed value", "B": "A container that stores data that can change", "C": "A function", "D": "A loop"},
            correct_answer="B", explanation="A variable is a named container that stores data. The value can change during program execution.", is_active=True),
        Assessment(module_id=11, question_text="What is a function in programming?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=2, points=10,
            options={"A": "A variable", "B": "A reusable block of code that performs a specific task", "C": "A data type", "D": "A loop"},
            correct_answer="B", explanation="A function is a reusable block of code that performs a specific task when called, helping to organize and modularize code.", is_active=True),
        Assessment(module_id=11, question_text="What does HTML stand for?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=3, points=10,
            options={"A": "HyperText Markup Language", "B": "High Tech Modern Language", "C": "Home Tool Markup Language", "D": "Hyper Transfer Markup Language"},
            correct_answer="A", explanation="HTML (HyperText Markup Language) is the standard markup language for creating web pages and web applications.", is_active=True),
        Assessment(module_id=11, question_text="What is the purpose of CSS?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=4, points=10,
            options={"A": "To structure web pages", "B": "To style and format the appearance of web pages", "C": "To add interactivity", "D": "To store data"},
            correct_answer="B", explanation="CSS (Cascading Style Sheets) is used to style and format the visual appearance of HTML elements on web pages.", is_active=True),
        Assessment(module_id=11, question_text="How is JavaScript used across the stack?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=5, points=10,
            options={"A": "It only runs in web browsers", "B": "It can power front-end, back-end (via Node.js), and even smart contract tooling", "C": "It is only for styling web pages", "D": "It is exclusively for database management"},
            correct_answer="B", explanation="JavaScript is versatile—used in browsers, servers (Node.js), build tooling, and scripting smart contract workflows.", is_active=True),
        Assessment(module_id=11, question_text="What is the purpose of loops in programming?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=6, points=10,
            options={"A": "To stop code execution", "B": "To execute a block of code repeatedly while a condition is met", "C": "To store static data", "D": "To compile programs"},
            correct_answer="B", explanation="Loops such as `for` or `while` iterate over code blocks, enabling repetitive tasks like processing arrays.", is_active=True),
        Assessment(module_id=11, question_text="Why is Node.js commonly installed for blockchain development?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=7, points=10,
            options={"A": "It is required to use HTML and CSS", "B": "Node.js provides package managers and tooling (npm/yarn) used by smart contract frameworks", "C": "Node.js replaces the need for Solidity", "D": "Node.js runs directly on-chain"},
            correct_answer="B", explanation="Smart contract frameworks rely on Node.js tooling for compilation, testing, and deployment scripts.", is_active=True),
        Assessment(module_id=11, question_text="How do HTML, CSS, and JavaScript collaborate in web development?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=8, points=10,
            options={"A": "HTML styles pages, CSS adds interactivity, JavaScript structures content", "B": "HTML structures content, CSS handles presentation, JavaScript adds interactivity", "C": "HTML stores data, CSS queries databases, JavaScript compiles code", "D": "They are interchangeable technologies"},
            correct_answer="B", explanation="HTML defines structure, CSS styles the appearance, and JavaScript adds dynamic behavior and logic.", is_active=True),
        Assessment(module_id=11, question_text="What role do data structures play in programming?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=9, points=10,
            options={"A": "They determine a program's color scheme", "B": "They organize and store data efficiently, e.g., arrays or maps", "C": "They only exist in spreadsheets", "D": "They are obsolete in modern languages"},
            correct_answer="B", explanation="Data structures such as arrays, objects, maps, and sets help organize data for efficient access and manipulation.", is_active=True),
        Assessment(module_id=11, question_text="Why are programming fundamentals important before writing smart contracts?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=10, points=10,
            options={"A": "Smart contracts require no prior programming knowledge", "B": "Understanding variables, control flow, and debugging is essential for secure smart contract code", "C": "Because smart contracts are written in HTML", "D": "So you can avoid using testing frameworks"},
            correct_answer="B", explanation="Smart contracts are code executed on-chain; strong fundamentals help avoid logical bugs and security vulnerabilities.", is_active=True),
    ]


def get_module_12_assessments() -> List[Assessment]:
    """Module 12: Smart Contract Development (Solidity & EVM) - 10 questions"""
    return [
        Assessment(module_id=12, question_text="What is Solidity?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=1, points=10,
            options={"A": "A blockchain", "B": "The programming language for writing Ethereum smart contracts", "C": "A wallet", "D": "A token standard"},
            correct_answer="B", explanation="Solidity is the primary programming language used to write smart contracts on Ethereum and EVM-compatible blockchains.", is_active=True),
        Assessment(module_id=12, question_text="What is the EVM (Ethereum Virtual Machine)?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=2, points=10,
            options={"A": "A physical computer", "B": "The runtime environment that executes smart contracts on Ethereum", "C": "A cryptocurrency", "D": "A wallet"},
            correct_answer="B", explanation="The EVM is the virtual machine that executes smart contract code on the Ethereum network, ensuring consistent execution across all nodes.", is_active=True),
        Assessment(module_id=12, question_text="What is a re-entrancy attack?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=3, points=10,
            options={"A": "A type of token", "B": "An attack where a contract calls back into itself before completing, potentially draining funds", "C": "A wallet hack", "D": "A blockchain feature"},
            correct_answer="B", explanation="Re-entrancy attacks occur when a malicious contract calls back into the vulnerable contract before state updates complete, potentially draining funds.", is_active=True),
        Assessment(module_id=12, question_text="What is a modifier in Solidity?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=4, points=10,
            options={"A": "A variable", "B": "A reusable code block that adds conditions to functions", "C": "A function", "D": "A data type"},
            correct_answer="B", explanation="Modifiers are reusable code blocks that add conditions (like access control) to functions, making code more secure and organized.", is_active=True),
        Assessment(module_id=12, question_text="Why is smart contract immutability significant?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=5, points=10,
            options={"A": "Code can be edited on-chain after deployment", "B": "Once deployed, contract code cannot be changed, so bugs persist", "C": "Immutability only applies to testnets", "D": "It means contracts do not store state"},
            correct_answer="B", explanation="Deployed contracts are immutable, so vulnerabilities remain unless upgradable patterns are carefully implemented. Thorough testing is essential.", is_active=True),
        Assessment(module_id=12, question_text="Are smart contracts automatically secure?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=6, points=10,
            options={"A": "Yes, the blockchain secures them by default", "B": "No, developers must guard against issues like re-entrancy, overflow, and access control flaws", "C": "Security depends solely on gas price", "D": "Only layer-2 contracts can be hacked"},
            correct_answer="B", explanation="Smart contracts require careful design, audits, and testing to avoid exploitable vulnerabilities.", is_active=True),
        Assessment(module_id=12, question_text="Which statement describes Solidity inheritance?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=7, points=10,
            options={"A": "Solidity does not support inheritance", "B": "Contracts can inherit functions and state from parent contracts to promote reuse", "C": "Inheritance only works for variables, not functions", "D": "Inheritance automatically prevents bugs"},
            correct_answer="B", explanation="Solidity supports single and multiple inheritance, enabling developers to share logic across contracts.", is_active=True),
        Assessment(module_id=12, question_text="Why is smart contract security critical?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=8, points=10,
            options={"A": "Contracts can be patched instantly after deployment", "B": "Bugs can lead to irreversible fund loss because code execution is immutable", "C": "Security is managed entirely by miners", "D": "Only front-end code needs security"},
            correct_answer="B", explanation="Exploiters can drain funds if vulnerabilities exist, and immutable code means issues cannot easily be fixed post-deployment.", is_active=True),
        Assessment(module_id=12, question_text="What is the purpose of events in Solidity?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=9, points=10,
            options={"A": "To store private keys on-chain", "B": "To log state changes for off-chain services like front-ends and indexers", "C": "To replace require statements", "D": "To reduce gas fees automatically"},
            correct_answer="B", explanation="Events emit logs that off-chain applications monitor to update UIs and maintain history without reading storage repeatedly.", is_active=True),
        Assessment(module_id=12, question_text="How do view, pure, and payable functions differ in Solidity?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=10, points=10,
            options={"A": "View modifies state, pure reads state, payable deletes state", "B": "View reads state, pure accesses no state, payable accepts Ether transfers", "C": "All three have identical behavior", "D": "Payable functions cannot receive Ether"},
            correct_answer="B", explanation="View functions read state, pure functions neither read nor modify state, and payable functions can receive Ether.", is_active=True),
    ]


def get_module_13_assessments() -> List[Assessment]:
    """Module 13: dApp Development & Tooling - 10 questions"""
    return [
        Assessment(module_id=13, question_text="What is Hardhat?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=1, points=10,
            options={"A": "A cryptocurrency", "B": "A development framework for compiling, testing, and deploying smart contracts", "C": "A wallet", "D": "A blockchain"},
            correct_answer="B", explanation="Hardhat is a popular development environment and testing framework for Ethereum smart contracts.", is_active=True),
        Assessment(module_id=13, question_text="What is Ethers.js?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=2, points=10,
            options={"A": "A blockchain", "B": "A JavaScript library for interacting with Ethereum and smart contracts", "C": "A wallet", "D": "A token"},
            correct_answer="B", explanation="Ethers.js is a JavaScript library that provides tools to connect web applications to Ethereum and interact with smart contracts.", is_active=True),
        Assessment(module_id=13, question_text="What is the purpose of a front-end in a dApp?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=3, points=10,
            options={"A": "To store data", "B": "To provide a user interface for interacting with smart contracts", "C": "To mine blocks", "D": "To validate transactions"},
            correct_answer="B", explanation="The front-end provides the user interface that allows users to interact with smart contracts through their wallets.", is_active=True),
        Assessment(module_id=13, question_text="What does 'connecting a wallet' mean in a dApp?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=4, points=10,
            options={"A": "Creating a new wallet", "B": "Linking your wallet to the dApp to sign transactions and interact with smart contracts", "C": "Sending funds", "D": "Installing software"},
            correct_answer="B", explanation="Connecting a wallet links your wallet to the dApp, allowing it to request transaction signatures and interact with smart contracts on your behalf.", is_active=True),
        Assessment(module_id=13, question_text="How can developers safely test smart contracts before mainnet deployment?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=5, points=10,
            options={"A": "They cannot test before mainnet", "B": "By using local networks or testnets provided by tools like Hardhat or Foundry", "C": "By deploying directly to mainnet without tests", "D": "By using a centralized database"},
            correct_answer="B", explanation="Frameworks support local test networks and public testnets where contracts can be deployed and tested without risking real funds.", is_active=True),
        Assessment(module_id=13, question_text="Why do many dApps rely on smart contracts instead of traditional servers?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=6, points=10,
            options={"A": "Smart contracts provide decentralized execution and trustless automation", "B": "Smart contracts are easier to scale than HTML", "C": "Traditional servers cannot store data", "D": "Smart contracts remove the need for wallets"},
            correct_answer="A", explanation="Smart contracts run on the blockchain, executing transparently and trustlessly without centralized control, though auxiliary servers may still be used.", is_active=True),
        Assessment(module_id=13, question_text="How do Web3.js and Ethers.js compare?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=7, points=10,
            options={"A": "They serve identical roles as libraries for Ethereum interaction, with different APIs and design choices", "B": "Web3.js is for Bitcoin, Ethers.js is for Ethereum", "C": "Only Web3.js can connect wallets", "D": "Ethers.js cannot read contract state"},
            correct_answer="A", explanation="Both libraries facilitate communication with Ethereum nodes, though they differ in ergonomics and architecture.", is_active=True),
        Assessment(module_id=13, question_text="What is a typical workflow for building a dApp?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=8, points=10,
            options={"A": "Skip testing and deploy directly to mainnet", "B": "Write smart contracts, test locally, deploy to testnet, build the front-end, integrate wallet interactions, then deploy to mainnet", "C": "Only build the front-end and ignore smart contracts", "D": "Deploy back-end first then write the smart contracts"},
            correct_answer="B", explanation="A robust workflow includes iterative testing, front-end integration, and staged deployments from local to testnet to mainnet environments.", is_active=True),
        Assessment(module_id=13, question_text="What benefits do frameworks like Hardhat or Foundry provide?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=9, points=10,
            options={"A": "They host smart contracts on centralized servers", "B": "They compile contracts, run automated tests, manage deployments, and offer debugging tools", "C": "They only create NFTs", "D": "They eliminate the need for wallets"},
            correct_answer="B", explanation="Development frameworks streamline contract compilation, testing, deployment scripting, and debugging, accelerating development cycles.", is_active=True),
        Assessment(module_id=13, question_text="How does a front-end communicate with a smart contract?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=10, points=10,
            options={"A": "Through HTML forms only", "B": "Using libraries such as Ethers.js/Web3.js with a provider, contract ABI, and wallet signatures for transactions", "C": "By emailing transaction details to miners", "D": "By storing the contract in local storage"},
            correct_answer="B", explanation="Front-ends load the contract ABI, connect through an RPC provider, and request signatures from the user's wallet to read/write contract state.", is_active=True),
    ]


def get_module_14_assessments() -> List[Assessment]:
    """Module 14: Creating a Fungible Token & ICO - 10 questions"""
    return [
        Assessment(module_id=14, question_text="What is the ERC-20 standard?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=1, points=10,
            options={"A": "A type of NFT", "B": "A standard interface for fungible tokens on Ethereum", "C": "A blockchain", "D": "A wallet"},
            correct_answer="B", explanation="ERC-20 defines a standard interface that all fungible tokens on Ethereum must implement, ensuring compatibility across the ecosystem.", is_active=True),
        Assessment(module_id=14, question_text="What is the 'transfer' function in ERC-20?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=2, points=10,
            options={"A": "A function to receive tokens", "B": "A function to send tokens from your address to another address", "C": "A function to create tokens", "D": "A function to burn tokens"},
            correct_answer="B", explanation="The transfer function allows the token owner to send tokens from their address to another address.", is_active=True),
        Assessment(module_id=14, question_text="What is an ICO (Initial Coin Offering)?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=3, points=10,
            options={"A": "A type of wallet", "B": "A fundraising mechanism where a project sells tokens to raise capital", "C": "A blockchain", "D": "A smart contract standard"},
            correct_answer="B", explanation="An ICO is a fundraising method where projects sell tokens to investors to raise capital for development.", is_active=True),
        Assessment(module_id=14, question_text="What is the 'approve' function used for in ERC-20?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=4, points=10,
            options={"A": "To transfer tokens", "B": "To allow another address to spend tokens on your behalf", "C": "To create tokens", "D": "To burn tokens"},
            correct_answer="B", explanation="The approve function allows you to authorize another address (like a DEX) to spend a specific amount of your tokens.", is_active=True),
        Assessment(module_id=14, question_text="Which functions are required by the ERC-20 standard?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=5, points=10,
            options={"A": "Only totalSupply", "B": "Functions like transfer, approve, transferFrom, balanceOf, allowance, and events", "C": "No functions are specified", "D": "Only mint and burn"},
            correct_answer="B", explanation="ERC-20 defines a consistent interface, including transfer, transferFrom, approve, balanceOf, allowance, and related events.", is_active=True),
        Assessment(module_id=14, question_text="Can you launch an ERC-20 token without writing or deploying contract code?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=6, points=10,
            options={"A": "Yes, tokens appear automatically", "B": "No, you must deploy a smart contract (even if using templates or generators)", "C": "Only centralized exchanges can create tokens", "D": "Smart contracts are optional for tokens"},
            correct_answer="B", explanation="Creating a token requires deploying contract code, though boilerplates and launch tools can simplify the process.", is_active=True),
        Assessment(module_id=14, question_text="How do ICO regulations vary globally?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=7, points=10,
            options={"A": "All countries follow identical ICO regulations", "B": "Regulatory treatment differs by jurisdiction; some countries have strict rules while others are permissive", "C": "ICOs are illegal everywhere", "D": "Only decentralized protocols regulate ICOs"},
            correct_answer="B", explanation="Legal frameworks differ worldwide, so projects must understand and comply with local regulatory requirements.", is_active=True),
        Assessment(module_id=14, question_text="Which components are essential in an ERC-20 token smart contract?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=8, points=10,
            options={"A": "Only a single transfer function", "B": "State variables and functions for supply tracking, balances, transfers, approvals, and events", "C": "Just a website", "D": "Only constructor logic"},
            correct_answer="B", explanation="A compliant token tracks total supply, balances, allowances, and emits events to signal transfers and approvals.", is_active=True),
        Assessment(module_id=14, question_text="What typically defines an ICO smart contract?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=9, points=10,
            options={"A": "Only a marketing page", "B": "Parameters for token price, contribution tracking, caps, timelines, and distribution logic", "C": "A centralized database of investors", "D": "Miners approving contributions manually"},
            correct_answer="B", explanation="ICO contracts manage token sales by defining pricing, caps, timelines, investor contributions, and distribution mechanics.", is_active=True),
        Assessment(module_id=14, question_text="Which security practices help protect an ERC-20 token launch?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=10, points=10,
            options={"A": "Skipping audits to save time", "B": "Implementing audits, access control, overflow checks, and secure deployment procedures", "C": "Relying solely on centralized administrators", "D": "Avoiding unit tests"},
            correct_answer="B", explanation="Thorough audits, rigorous testing, role-based access control, and secure deployment reduce the likelihood of vulnerabilities.", is_active=True),
    ]


def get_module_15_assessments() -> List[Assessment]:
    """Module 15: Creating an NFT Collection & Marketplace - 10 questions"""
    return [
        Assessment(module_id=15, question_text="What is the ERC-721 standard?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=1, points=10,
            options={"A": "A fungible token standard", "B": "A standard for non-fungible tokens (NFTs) on Ethereum", "C": "A blockchain", "D": "A wallet"},
            correct_answer="B", explanation="ERC-721 is the standard interface for non-fungible tokens (NFTs) on Ethereum, ensuring each token is unique.", is_active=True),
        Assessment(module_id=15, question_text="What is IPFS?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=2, points=10,
            options={"A": "A blockchain", "B": "InterPlanetary File System - a decentralized storage network for NFT metadata and images", "C": "A token standard", "D": "A wallet"},
            correct_answer="B", explanation="IPFS is a peer-to-peer distributed file system used to store NFT images and metadata in a decentralized way.", is_active=True),
        Assessment(module_id=15, question_text="What is NFT metadata?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=3, points=10,
            options={"A": "The token itself", "B": "Data that describes the NFT (name, description, image URL, attributes)", "C": "The blockchain", "D": "A wallet address"},
            correct_answer="B", explanation="Metadata contains information about the NFT including its name, description, image location, and attributes that define what it represents.", is_active=True),
        Assessment(module_id=15, question_text="What is the difference between ERC-721 and ERC-1155?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=4, points=10,
            options={"A": "There is no difference", "B": "ERC-721 is for unique NFTs, ERC-1155 supports both fungible and non-fungible tokens in one contract", "C": "ERC-721 is newer", "D": "ERC-1155 is only for fungible tokens"},
            correct_answer="B", explanation="ERC-721 handles only unique NFTs. ERC-1155 is a hybrid standard that can handle both fungible and non-fungible tokens in a single contract.", is_active=True),
        Assessment(module_id=15, question_text="Where are NFT media files typically stored?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=5, points=10,
            options={"A": "Directly inside the token on-chain", "B": "On decentralized storage like IPFS, referenced by on-chain metadata", "C": "Only on centralized servers", "D": "Within the miner's hardware wallet"},
            correct_answer="B", explanation="Due to cost and size, NFTs store a reference (e.g., IPFS hash) on-chain while the actual media resides in decentralized storage.", is_active=True),
        Assessment(module_id=15, question_text="Why do NFT marketplaces rely on smart contracts?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=6, points=10,
            options={"A": "Smart contracts handle listing, bids, transfers, and payouts trustlessly", "B": "Smart contracts only host marketing pages", "C": "Marketplaces use spreadsheets instead", "D": "Smart contracts are optional overhead"},
            correct_answer="A", explanation="Marketplace contracts enforce rules for listing, buying, royalties, and transfers in a transparent, automated way.", is_active=True),
        Assessment(module_id=15, question_text="Do NFTs in the same collection need identical metadata?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=7, points=10,
            options={"A": "Yes, every NFT has identical metadata", "B": "No, each NFT can have unique attributes while sharing the same contract", "C": "Metadata is not used in NFT collections", "D": "Only images can differ"},
            correct_answer="B", explanation="Collections often share a base contract but each token may have unique names, traits, and media references.", is_active=True),
        Assessment(module_id=15, question_text="Why is IPFS commonly used for NFT metadata?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=8, points=10,
            options={"A": "It is more expensive than on-chain storage", "B": "IPFS provides decentralized, content-addressed storage that is resilient and cost-effective", "C": "Only centralized storage is reliable", "D": "IPFS automatically mints NFTs"},
            correct_answer="B", explanation="IPFS offers decentralized storage with content hashing, ensuring metadata remains accessible and tamper-resistant.", is_active=True),
        Assessment(module_id=15, question_text="Which functions are typically implemented in an NFT marketplace contract?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=9, points=10,
            options={"A": "Functions for listing, buying, canceling listings, transferring ownership, and handling fees", "B": "Only a single mint function", "C": "Functions for mining blocks", "D": "There are no smart contract functions in marketplaces"},
            correct_answer="A", explanation="Marketplace contracts handle listing management, purchases, cancellations, royalties, and fee settlements.", is_active=True),
        Assessment(module_id=15, question_text="What are the high-level steps to launch an NFT collection?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=10, points=10,
            options={"A": "Deploy contract first without metadata", "B": "Design assets, generate metadata, upload to IPFS, deploy ERC-721 contract, mint, and verify", "C": "Only create a website", "D": "Mint NFTs without a smart contract"},
            correct_answer="B", explanation="Successful launches require asset creation, metadata preparation, decentralized storage, contract deployment, minting, and verification.", is_active=True),
    ]


def get_module_16_assessments() -> List[Assessment]:
    """Module 16: Building Your Own Blockchain & Mining - 10 questions"""
    return [
        Assessment(module_id=16, question_text="What are the main components of a blockchain?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=1, points=10,
            options={"A": "Only blocks", "B": "Blocks, cryptographic hashing, consensus mechanism, network of nodes", "C": "Only nodes", "D": "Only consensus"},
            correct_answer="B", explanation="A blockchain consists of blocks linked by hashes, a consensus mechanism for agreement, and a network of nodes that maintain the ledger.", is_active=True),
        Assessment(module_id=16, question_text="What is a hash in blockchain?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=2, points=10,
            options={"A": "A type of transaction", "B": "A cryptographic function that converts data into a fixed-size string, used to link blocks", "C": "A wallet", "D": "A token"},
            correct_answer="B", explanation="A hash is a one-way cryptographic function that converts data into a fixed-size string, creating the links between blocks in a chain.", is_active=True),
        Assessment(module_id=16, question_text="What is a mining pool?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=3, points=10,
            options={"A": "A swimming pool", "B": "A group of miners who combine computational power to increase chances of finding blocks and share rewards", "C": "A type of wallet", "D": "A blockchain"},
            correct_answer="B", explanation="Mining pools combine the hashing power of multiple miners to increase the probability of finding blocks, with rewards distributed based on contribution.", is_active=True),
        Assessment(module_id=16, question_text="What is the purpose of the nonce in Proof-of-Work?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=4, points=10,
            options={"A": "To store transactions", "B": "A number that miners change to find a valid block hash", "C": "A wallet address", "D": "A token"},
            correct_answer="B", explanation="The nonce is a number that miners increment to find a hash that meets the network's difficulty requirement, proving work was done.", is_active=True),
        Assessment(module_id=16, question_text="How can building a simple blockchain prototype help learners?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=5, points=10,
            options={"A": "It provides no educational value", "B": "It illustrates how blocks, hashes, and consensus tie together", "C": "It replaces the need to study cryptography", "D": "It automatically deploys on mainnet"},
            correct_answer="B", explanation="Hands-on prototypes clarify how blocks reference previous hashes, how validation works, and why consensus is required.", is_active=True),
        Assessment(module_id=16, question_text="Which factors influence mining profitability?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=6, points=10,
            options={"A": "Only the market price of the coin", "B": "Hardware efficiency, electricity cost, network difficulty, block rewards, and coin price", "C": "The color of the mining rig", "D": "Weather conditions in data centers"},
            correct_answer="B", explanation="Profitability depends on revenue from block rewards minus electricity and hardware costs, adjusted for difficulty and market price.", is_active=True),
        Assessment(module_id=16, question_text="Do all blockchains rely on the same consensus mechanism?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=7, points=10,
            options={"A": "Yes, all blockchains use Proof-of-Work", "B": "No, consensus mechanisms vary (PoW, PoS, DPoS, PoA, etc.) depending on design goals", "C": "Consensus is optional for blockchains", "D": "Only private blockchains use consensus"},
            correct_answer="B", explanation="Different networks choose consensus mechanisms that balance security, decentralization, and performance according to their objectives.", is_active=True),
        Assessment(module_id=16, question_text="How are blocks chained together securely?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=8, points=10,
            options={"A": "Blocks are stored randomly", "B": "Each block references the previous block's hash, forming a tamper-evident chain", "C": "Blocks are linked by user passwords", "D": "Blocks are manually reordered weekly"},
            correct_answer="B", explanation="By including the previous block's hash, any modification breaks the chain, enabling integrity checks.", is_active=True),
        Assessment(module_id=16, question_text="What inputs are considered when estimating mining profitability?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=9, points=10,
            options={"A": "Only hash rate", "B": "Hash rate, power consumption, electricity cost, network difficulty, block reward, and coin price", "C": "The number of wallet addresses", "D": "User interface design"},
            correct_answer="B", explanation="Profit calculators use hash rate, power usage, cost of electricity, and network metrics to project earnings.", is_active=True),
        Assessment(module_id=16, question_text="What are the basic steps to build a simple blockchain implementation?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=10, points=10,
            options={"A": "Create a website and call it a blockchain", "B": "Define block structure, hash blocks, create a genesis block, link subsequent blocks, and implement validation rules", "C": "Only write a smart contract", "D": "Use a spreadsheet to list transactions"},
            correct_answer="B", explanation="A basic blockchain involves defining block data, hashing, linking via previous hashes, and validating the chain according to consensus rules.", is_active=True),
    ]


def get_module_17_assessments() -> List[Assessment]:
    """Module 17: AI Agent Application Development - 10 questions"""
    return [
        Assessment(module_id=17, question_text="What is an AI agent in the context of trading bots?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=1, points=10,
            options={"A": "A human trader", "B": "An autonomous system that can make decisions and take actions based on data and goals", "C": "A type of cryptocurrency", "D": "A wallet"},
            correct_answer="B", explanation="An AI agent is an autonomous system that can analyze data, make decisions, and execute actions (like trades) based on predefined goals and strategies.", is_active=True),
        Assessment(module_id=17, question_text="What is sentiment analysis?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=2, points=10,
            options={"A": "Analyzing prices", "B": "Analyzing social media and news to determine market sentiment (positive/negative)", "C": "Analyzing wallets", "D": "Analyzing transactions"},
            correct_answer="B", explanation="Sentiment analysis uses natural language processing to analyze social media, news, and other text sources to gauge market sentiment.", is_active=True),
        Assessment(module_id=17, question_text="What does 'LLM-agnostic' mean in the context of AI agents?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=3, points=10,
            options={"A": "Not using LLMs", "B": "Designed to work with any Large Language Model (OpenAI, Claude, Ollama, etc.)", "C": "Only using one LLM", "D": "A type of model"},
            correct_answer="B", explanation="LLM-agnostic means the system is designed to work with multiple LLM providers, not locked to one specific model or service.", is_active=True),
        Assessment(module_id=17, question_text="What is backtesting?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=4, points=10,
            options={"A": "Testing in the future", "B": "Testing a trading strategy against historical data to evaluate performance", "C": "Testing wallets", "D": "Testing blockchains"},
            correct_answer="B", explanation="Backtesting involves running a trading strategy against historical market data to see how it would have performed before risking real capital.", is_active=True),
        Assessment(module_id=17, question_text="What level of profit can AI trading bots guarantee?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=5, points=10,
            options={"A": "Guaranteed profits with no risk", "B": "Profits only during bull markets", "C": "No guarantees—bots are subject to market risk and strategy quality", "D": "Profits determined by transaction fees"},
            correct_answer="C", explanation="AI bots help automate strategies but cannot eliminate market risk; performance depends on data, strategy design, and risk controls.", is_active=True),
        Assessment(module_id=17, question_text="Why integrate multiple data sources into an AI agent?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=6, points=10,
            options={"A": "To confuse the model", "B": "To capture a fuller market picture by combining price, sentiment, and on-chain signals", "C": "To increase latency without benefit", "D": "To avoid using historical data"},
            correct_answer="B", explanation="Blending diverse data sets reduces blind spots and helps the agent validate signals before acting.", is_active=True),
        Assessment(module_id=17, question_text="How critical is risk management in trading bot development?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=7, points=10,
            options={"A": "Optional because bots always follow rules", "B": "Essential to control position sizing, drawdowns, and stop losses", "C": "Only necessary for manual trading", "D": "Irrelevant if the bot uses AI"},
            correct_answer="B", explanation="Risk frameworks prevent catastrophic losses and ensure the bot operates within acceptable limits.", is_active=True),
        Assessment(module_id=17, question_text="Why should an AI trading bot analyze technical indicators?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=8, points=10,
            options={"A": "Indicators provide mathematical insights into trends, momentum, and potential reversal points", "B": "Indicators replace the need for data", "C": "Indicators guarantee profits instantly", "D": "Indicators are only for human traders"},
            correct_answer="A", explanation="Technical indicators quantify market dynamics, helping bots detect trends and momentum for signal generation.", is_active=True),
        Assessment(module_id=17, question_text="Which components typically form a robust AI trading bot architecture?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=9, points=10,
            options={"A": "Only a user interface", "B": "Data ingestion, analysis engine, decision logic, risk management, execution, monitoring, and logging", "C": "Just a spreadsheet", "D": "Only a wallet connection"},
            correct_answer="B", explanation="A complete system ingests data, analyzes signals, executes trades, enforces risk controls, and logs performance for review.", is_active=True),
        Assessment(module_id=17, question_text="What role does backtesting play in AI trading bot development?", question_type=QuestionType.MULTIPLE_CHOICE, order_index=10, points=10,
            options={"A": "It is unnecessary if you have live capital", "B": "It evaluates strategies on historical data to understand performance before deployment", "C": "It guarantees future profits", "D": "It only applies to manual trading"},
            correct_answer="B", explanation="Backtesting lets developers assess how a strategy would have performed historically, revealing strengths and weaknesses before live trading.", is_active=True),
    ]


