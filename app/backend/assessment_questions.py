"""Comprehensive assessment questions for all modules (170 total)"""
from typing import List
from app.backend.models.assessment import Assessment, QuestionType


def get_all_assessments() -> dict[int, List[Assessment]]:
    """Returns a dictionary mapping module_id to list of Assessment objects"""
    assessments = {}
    
    # Module 1 is already defined in seed_local.py, so we start with Module 2
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
    """Module 2: Web3 Wallets & Security - 10 questions"""
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
        Assessment(module_id=2, question_text="True or False: You should store your seed phrase digitally (screenshot, email, cloud storage).", question_type=QuestionType.TRUE_FALSE, order_index=5, points=10,
            options=None, correct_answer="False", explanation="Seed phrases should be stored offline and physically. Digital storage makes them vulnerable to hackers.", is_active=True),
        Assessment(module_id=2, question_text="True or False: 'Not your keys, not your coins' means you don't own cryptocurrency stored in a custodial wallet.", question_type=QuestionType.TRUE_FALSE, order_index=6, points=10,
            options=None, correct_answer="True", explanation="If you don't control the private keys, you don't truly own the cryptocurrency. The custodian has control and could potentially freeze or lose your funds.", is_active=True),
        Assessment(module_id=2, question_text="True or False: You can recover your wallet if you lose your private key but have your seed phrase.", question_type=QuestionType.TRUE_FALSE, order_index=7, points=10,
            options=None, correct_answer="True", explanation="The seed phrase can regenerate all your private keys, so you can recover your entire wallet with just the seed phrase.", is_active=True),
        Assessment(module_id=2, question_text="Explain why it's important to never share your private key or seed phrase with anyone.", question_type=QuestionType.SHORT_ANSWER, order_index=8, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: private key gives complete control, no recovery mechanism, permanent loss if compromised.", is_active=True),
        Assessment(module_id=2, question_text="Describe the difference between a hot wallet and a cold wallet, and when you might use each.", question_type=QuestionType.SHORT_ANSWER, order_index=9, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: hot wallets are connected to internet (convenient for daily use), cold wallets are offline (secure for long-term storage).", is_active=True),
        Assessment(module_id=2, question_text="What are some common scams in Web3 and how can you protect yourself?", question_type=QuestionType.SHORT_ANSWER, order_index=10, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: phishing, fake airdrops, malicious contracts, social engineering. Protection: verify URLs, never share keys, research before interacting.", is_active=True),
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
        Assessment(module_id=3, question_text="True or False: Gas fees are fixed and never change.", question_type=QuestionType.TRUE_FALSE, order_index=5, points=10,
            options=None, correct_answer="False", explanation="Gas fees fluctuate based on supply and demand. When network activity is high, gas fees increase.", is_active=True),
        Assessment(module_id=3, question_text="True or False: Layer-2 solutions help reduce gas fees and increase transaction speed.", question_type=QuestionType.TRUE_FALSE, order_index=6, points=10,
            options=None, correct_answer="True", explanation="Layer-2 solutions process transactions off the main chain, reducing congestion and lowering fees while maintaining security.", is_active=True),
        Assessment(module_id=3, question_text="True or False: All dApps require you to connect your wallet to use them.", question_type=QuestionType.TRUE_FALSE, order_index=7, points=10,
            options=None, correct_answer="True", explanation="dApps require wallet connection to interact with smart contracts, sign transactions, and pay gas fees.", is_active=True),
        Assessment(module_id=3, question_text="Explain how gas fees are calculated and what factors influence them.", question_type=QuestionType.SHORT_ANSWER, order_index=8, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: network congestion, transaction complexity, gas price (gwei), supply and demand.", is_active=True),
        Assessment(module_id=3, question_text="What is the purpose of Layer-2 scaling solutions, and give one example.", question_type=QuestionType.SHORT_ANSWER, order_index=9, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: reduce congestion, lower fees, faster transactions. Examples: rollups, sidechains, state channels.", is_active=True),
        Assessment(module_id=3, question_text="Describe the difference between a traditional app and a dApp.", question_type=QuestionType.SHORT_ANSWER, order_index=10, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: dApps run on blockchain, use smart contracts, decentralized backend, require wallet connection, transparent and trustless.", is_active=True),
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
        Assessment(module_id=4, question_text="True or False: When you buy an NFT, you own the actual image file.", question_type=QuestionType.TRUE_FALSE, order_index=5, points=10,
            options=None, correct_answer="False", explanation="You own the token (receipt) that points to the image. The image itself is typically stored separately (often on IPFS).", is_active=True),
        Assessment(module_id=4, question_text="True or False: Stablecoins are tokens pegged 1:1 to a fiat currency like USD.", question_type=QuestionType.TRUE_FALSE, order_index=6, points=10,
            options=None, correct_answer="True", explanation="Stablecoins like USDC and USDT are designed to maintain a 1:1 peg with the US dollar to provide price stability.", is_active=True),
        Assessment(module_id=4, question_text="True or False: All tokens on Ethereum use the ERC-20 standard.", question_type=QuestionType.TRUE_FALSE, order_index=7, points=10,
            options=None, correct_answer="False", explanation="Ethereum has multiple token standards: ERC-20 for fungible tokens, ERC-721 for NFTs, ERC-1155 for hybrid tokens, etc.", is_active=True),
        Assessment(module_id=4, question_text="Explain the difference between utility tokens and governance tokens.", question_type=QuestionType.SHORT_ANSWER, order_index=8, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: utility tokens provide access to services, governance tokens give voting rights in DAOs.", is_active=True),
        Assessment(module_id=4, question_text="What is token burning and why do projects do it?", question_type=QuestionType.SHORT_ANSWER, order_index=9, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: permanently removing tokens from circulation, reducing supply, potentially increasing value, deflationary mechanism.", is_active=True),
        Assessment(module_id=4, question_text="Describe what metadata is in the context of NFTs and why it's important.", question_type=QuestionType.SHORT_ANSWER, order_index=10, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: metadata contains information about the NFT (name, description, image URL, attributes), stored on-chain or IPFS, defines what the NFT represents.", is_active=True),
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
        Assessment(module_id=5, question_text="True or False: DEXs require KYC (Know Your Customer) verification.", question_type=QuestionType.TRUE_FALSE, order_index=5, points=10,
            options=None, correct_answer="False", explanation="DEXs are non-custodial and typically don't require KYC since you're trading directly from your wallet without an intermediary.", is_active=True),
        Assessment(module_id=5, question_text="True or False: CEXs are generally faster and easier to use than DEXs for beginners.", question_type=QuestionType.TRUE_FALSE, order_index=6, points=10,
            options=None, correct_answer="True", explanation="CEXs offer fiat on-ramps, simpler interfaces, and customer support, making them more beginner-friendly despite being custodial.", is_active=True),
        Assessment(module_id=5, question_text="True or False: You should only invest money you can afford to lose in cryptocurrency trading.", question_type=QuestionType.TRUE_FALSE, order_index=7, points=10,
            options=None, correct_answer="True", explanation="Cryptocurrency is highly volatile and risky. Only invest what you can afford to lose completely.", is_active=True),
        Assessment(module_id=5, question_text="Explain the main pros and cons of using a CEX versus a DEX.", question_type=QuestionType.SHORT_ANSWER, order_index=8, points=10,
            options=None, correct_answer="", explanation="Instructor will review. CEX: pros (easy, fast, fiat on-ramp, support), cons (custodial, KYC, centralization risk). DEX: pros (non-custodial, no KYC, decentralized), cons (gas fees, complexity, no fiat).", is_active=True),
        Assessment(module_id=5, question_text="What is risk management in trading and why is it important?", question_type=QuestionType.SHORT_ANSWER, order_index=9, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: managing position sizes, setting stop losses, diversifying, avoiding emotional decisions, protecting capital.", is_active=True),
        Assessment(module_id=5, question_text="Describe what 'impermanent loss' means in the context of providing liquidity to a DEX.", question_type=QuestionType.SHORT_ANSWER, order_index=10, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: temporary loss when token prices change, occurs in liquidity pools, realized if you withdraw, vs holding tokens separately.", is_active=True),
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
        Assessment(module_id=6, question_text="True or False: In DeFi lending, you can borrow without providing collateral.", question_type=QuestionType.TRUE_FALSE, order_index=5, points=10,
            options=None, correct_answer="False", explanation="DeFi lending requires over-collateralization - you must lock up more value than you borrow to secure the loan.", is_active=True),
        Assessment(module_id=6, question_text="True or False: DAOs use governance tokens for voting on proposals.", question_type=QuestionType.TRUE_FALSE, order_index=6, points=10,
            options=None, correct_answer="True", explanation="DAOs use governance tokens to give holders voting rights on proposals, treasury management, and protocol changes.", is_active=True),
        Assessment(module_id=6, question_text="True or False: Impermanent loss only occurs when token prices go down.", question_type=QuestionType.TRUE_FALSE, order_index=7, points=10,
            options=None, correct_answer="False", explanation="Impermanent loss occurs when token prices change in either direction, not just down. It's the difference between holding tokens vs providing liquidity.", is_active=True),
        Assessment(module_id=6, question_text="Explain how DeFi lending and borrowing works differently from traditional banks.", question_type=QuestionType.SHORT_ANSWER, order_index=8, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: no credit checks, over-collateralization, automated smart contracts, global access, no intermediaries, transparent.", is_active=True),
        Assessment(module_id=6, question_text="What are the main risks associated with DeFi protocols?", question_type=QuestionType.SHORT_ANSWER, order_index=9, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: smart contract bugs, impermanent loss, protocol hacks, rug pulls, oracle failures, regulatory risk.", is_active=True),
        Assessment(module_id=6, question_text="Describe how a DAO makes decisions and manages its treasury.", question_type=QuestionType.SHORT_ANSWER, order_index=10, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: governance tokens for voting, proposals submitted, community votes, smart contracts execute decisions, treasury managed transparently on-chain.", is_active=True),
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
        Assessment(module_id=7, question_text="True or False: Blockchains are completely anonymous.", question_type=QuestionType.TRUE_FALSE, order_index=5, points=10,
            options=None, correct_answer="False", explanation="Blockchains are pseudonymous, not anonymous. All transactions are public and traceable, though identities aren't directly revealed.", is_active=True),
        Assessment(module_id=7, question_text="True or False: Mixers can help obscure transaction trails for privacy.", question_type=QuestionType.TRUE_FALSE, order_index=6, points=10,
            options=None, correct_answer="True", explanation="Mixers (or tumblers) combine multiple transactions to obscure the trail, though they have legitimate and illicit uses.", is_active=True),
        Assessment(module_id=7, question_text="True or False: Different blockchains can directly communicate with each other without bridges.", question_type=QuestionType.TRUE_FALSE, order_index=7, points=10,
            options=None, correct_answer="False", explanation="Blockchains operate independently. Bridges or other interoperability solutions are needed to transfer assets between chains.", is_active=True),
        Assessment(module_id=7, question_text="Explain why blockchain privacy is important and what tools exist to enhance it.", question_type=QuestionType.SHORT_ANSWER, order_index=8, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: financial privacy, protection from surveillance, mixers, ZKPs, privacy coins, transaction obfuscation.", is_active=True),
        Assessment(module_id=7, question_text="What are the main challenges with cross-chain interoperability and how do bridges address them?", question_type=QuestionType.SHORT_ANSWER, order_index=9, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: different consensus mechanisms, wrapped tokens, trust assumptions, security risks, complexity of bridging.", is_active=True),
        Assessment(module_id=7, question_text="Describe the difference between ASICs and GPUs in the context of Proof-of-Work mining.", question_type=QuestionType.SHORT_ANSWER, order_index=10, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: ASICs are specialized for specific algorithms (more efficient but less flexible), GPUs are general-purpose (more flexible but less efficient for specific tasks).", is_active=True),
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
        Assessment(module_id=8, question_text="True or False: Block explorers are run by the blockchain itself.", question_type=QuestionType.TRUE_FALSE, order_index=5, points=10,
            options=None, correct_answer="False", explanation="Block explorers are typically third-party services (like Etherscan) that index and display blockchain data. The blockchain itself is decentralized.", is_active=True),
        Assessment(module_id=8, question_text="True or False: You need to connect your wallet to use the 'Read Contract' tab.", question_type=QuestionType.TRUE_FALSE, order_index=6, points=10,
            options=None, correct_answer="False", explanation="The Read Contract tab is free and doesn't require wallet connection. Only Write Contract requires wallet connection and gas fees.", is_active=True),
        Assessment(module_id=8, question_text="True or False: All transactions on a blockchain are publicly visible.", question_type=QuestionType.TRUE_FALSE, order_index=7, points=10,
            options=None, correct_answer="True", explanation="On public blockchains, all transactions are visible to anyone. Privacy features may obscure details, but transactions are still recorded publicly.", is_active=True),
        Assessment(module_id=8, question_text="Explain how you would use a block explorer to verify a transaction before it's confirmed.", question_type=QuestionType.SHORT_ANSWER, order_index=8, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: search transaction hash, check status (pending/confirmed), view details, verify addresses and amounts.", is_active=True),
        Assessment(module_id=8, question_text="What information can you learn from analyzing a protocol's TVL and how is it useful?", question_type=QuestionType.SHORT_ANSWER, order_index=9, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: protocol size, user trust, growth trends, comparison with competitors, health indicator.", is_active=True),
        Assessment(module_id=8, question_text="Describe how you would trace funds from a suspicious wallet address to identify potential scams.", question_type=QuestionType.SHORT_ANSWER, order_index=10, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: view transaction history, follow incoming/outgoing transfers, check token movements, identify patterns, trace to known addresses (exchanges, other wallets).", is_active=True),
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
        Assessment(module_id=9, question_text="True or False: Technical Analysis can guarantee future price movements.", question_type=QuestionType.TRUE_FALSE, order_index=5, points=10,
            options=None, correct_answer="False", explanation="TA provides probabilities based on historical patterns but cannot guarantee future outcomes. Markets are unpredictable.", is_active=True),
        Assessment(module_id=9, question_text="True or False: Reading a project's whitepaper is part of Fundamental Analysis.", question_type=QuestionType.TRUE_FALSE, order_index=6, points=10,
            options=None, correct_answer="True", explanation="Whitepapers are a key source for FA as they explain the project's goals, technology, and tokenomics.", is_active=True),
        Assessment(module_id=9, question_text="True or False: High on-chain activity always indicates a bullish market.", question_type=QuestionType.TRUE_FALSE, order_index=7, points=10,
            options=None, correct_answer="False", explanation="High activity can indicate various things. Context matters - it could be selling pressure, network congestion, or genuine adoption.", is_active=True),
        Assessment(module_id=9, question_text="Explain the difference between support and resistance levels in trading.", question_type=QuestionType.SHORT_ANSWER, order_index=8, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: support is price level where buying pressure emerges (floor), resistance is where selling pressure emerges (ceiling).", is_active=True),
        Assessment(module_id=9, question_text="What should you look for when analyzing a project's tokenomics?", question_type=QuestionType.SHORT_ANSWER, order_index=9, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: total supply, distribution, vesting schedules, inflation/deflation mechanisms, utility, token allocation.", is_active=True),
        Assessment(module_id=9, question_text="How can on-chain metrics help you make better investment decisions?", question_type=QuestionType.SHORT_ANSWER, order_index=10, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: identify smart money, detect accumulation/distribution, measure network growth, assess adoption, gauge market sentiment.", is_active=True),
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
        Assessment(module_id=10, question_text="True or False: Leveraged strategies always increase your profits.", question_type=QuestionType.TRUE_FALSE, order_index=5, points=10,
            options=None, correct_answer="False", explanation="Leverage amplifies both gains and losses. While it can increase profits, it also significantly increases risk of liquidation.", is_active=True),
        Assessment(module_id=10, question_text="True or False: Delta-neutral strategies eliminate all risk.", question_type=QuestionType.TRUE_FALSE, order_index=6, points=10,
            options=None, correct_answer="False", explanation="Delta-neutral strategies reduce price risk but still face other risks like funding costs, impermanent loss, and protocol risks.", is_active=True),
        Assessment(module_id=10, question_text="True or False: All DeFi protocols have the same level of risk.", question_type=QuestionType.TRUE_FALSE, order_index=7, points=10,
            options=None, correct_answer="False", explanation="Protocols vary widely in risk based on code audits, track record, TVL, team, and economic design. Always assess each protocol individually.", is_active=True),
        Assessment(module_id=10, question_text="Explain what oracle risk is and why it matters in DeFi.", question_type=QuestionType.SHORT_ANSWER, order_index=8, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: oracles provide external data, manipulation risk, single point of failure, can cause protocol failures, importance of decentralized oracles.", is_active=True),
        Assessment(module_id=10, question_text="What factors should you consider when assessing protocol risk before investing?", question_type=QuestionType.SHORT_ANSWER, order_index=9, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: code audits, bug bounties, TVL, team reputation, economic design, insurance, track record, decentralization.", is_active=True),
        Assessment(module_id=10, question_text="Describe the risks and rewards of using leveraged yield farming strategies.", question_type=QuestionType.SHORT_ANSWER, order_index=10, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: rewards (amplified returns), risks (liquidation, higher borrowing costs, protocol risks, complexity, impermanent loss amplification).", is_active=True),
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
        Assessment(module_id=11, question_text="True or False: JavaScript is only used for front-end development.", question_type=QuestionType.TRUE_FALSE, order_index=5, points=10,
            options=None, correct_answer="False", explanation="JavaScript can be used for both front-end (browser) and back-end (Node.js) development, as well as smart contract development in some cases.", is_active=True),
        Assessment(module_id=11, question_text="True or False: A loop allows you to execute code multiple times.", question_type=QuestionType.TRUE_FALSE, order_index=6, points=10,
            options=None, correct_answer="True", explanation="Loops (for, while) allow you to repeat code execution multiple times, which is essential for processing collections of data.", is_active=True),
        Assessment(module_id=11, question_text="True or False: You need to install Node.js to develop smart contracts.", question_type=QuestionType.TRUE_FALSE, order_index=7, points=10,
            options=None, correct_answer="True", explanation="Node.js and npm/yarn are essential tools for smart contract development, testing frameworks, and building dApps.", is_active=True),
        Assessment(module_id=11, question_text="Explain the difference between HTML, CSS, and JavaScript in web development.", question_type=QuestionType.SHORT_ANSWER, order_index=8, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: HTML structures content, CSS styles appearance, JavaScript adds interactivity and functionality.", is_active=True),
        Assessment(module_id=11, question_text="What is the purpose of a data structure in programming and give one example.", question_type=QuestionType.SHORT_ANSWER, order_index=9, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: organize and store data efficiently. Examples: arrays, objects, lists, maps, sets.", is_active=True),
        Assessment(module_id=11, question_text="Why is understanding programming fundamentals important before learning smart contract development?", question_type=QuestionType.SHORT_ANSWER, order_index=10, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: smart contracts are code, need to understand logic, debugging, security, data structures, functions, error handling.", is_active=True),
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
        Assessment(module_id=12, question_text="True or False: Once deployed, a smart contract's code cannot be changed.", question_type=QuestionType.TRUE_FALSE, order_index=5, points=10,
            options=None, correct_answer="True", explanation="Smart contracts are immutable once deployed. This is why thorough testing and audits are critical before deployment.", is_active=True),
        Assessment(module_id=12, question_text="True or False: All smart contracts are secure by default.", question_type=QuestionType.TRUE_FALSE, order_index=6, points=10,
            options=None, correct_answer="False", explanation="Smart contracts require careful security practices. Common vulnerabilities include re-entrancy, overflow, and access control issues.", is_active=True),
        Assessment(module_id=12, question_text="True or False: Solidity supports inheritance, allowing contracts to inherit from other contracts.", question_type=QuestionType.TRUE_FALSE, order_index=7, points=10,
            options=None, correct_answer="True", explanation="Solidity supports inheritance, allowing contracts to inherit functions and state variables from parent contracts, promoting code reuse.", is_active=True),
        Assessment(module_id=12, question_text="Explain why smart contract security is critical and what can happen if a contract has vulnerabilities.", question_type=QuestionType.SHORT_ANSWER, order_index=8, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: immutable code, funds at risk, no recovery mechanism, hacks can drain contracts, importance of audits and testing.", is_active=True),
        Assessment(module_id=12, question_text="What is the purpose of events in Solidity and how are they useful?", question_type=QuestionType.SHORT_ANSWER, order_index=9, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: log important state changes, efficient for off-chain monitoring, front-end integration, debugging, gas-efficient logging.", is_active=True),
        Assessment(module_id=12, question_text="Describe the difference between view, pure, and payable functions in Solidity.", question_type=QuestionType.SHORT_ANSWER, order_index=10, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: view (reads state, no modification), pure (no state access), payable (can receive ETH).", is_active=True),
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
        Assessment(module_id=13, question_text="True or False: You can test smart contracts locally before deploying to mainnet.", question_type=QuestionType.TRUE_FALSE, order_index=5, points=10,
            options=None, correct_answer="True", explanation="Development frameworks like Hardhat allow you to test contracts on local networks or testnets before deploying to mainnet.", is_active=True),
        Assessment(module_id=13, question_text="True or False: dApps require a traditional backend server.", question_type=QuestionType.TRUE_FALSE, order_index=6, points=10,
            options=None, correct_answer="False", explanation="dApps use smart contracts as their backend, running on the blockchain. However, they may use centralized services for data indexing or APIs.", is_active=True),
        Assessment(module_id=13, question_text="True or False: Web3.js and Ethers.js serve the same purpose.", question_type=QuestionType.TRUE_FALSE, order_index=7, points=10,
            options=None, correct_answer="True", explanation="Both are JavaScript libraries for interacting with Ethereum, though they have different APIs and design philosophies.", is_active=True),
        Assessment(module_id=13, question_text="Explain the workflow of building and deploying a dApp from development to production.", question_type=QuestionType.SHORT_ANSWER, order_index=8, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: write smart contracts, test locally, deploy to testnet, build front-end, integrate wallet, test end-to-end, deploy to mainnet.", is_active=True),
        Assessment(module_id=13, question_text="What is the purpose of a development framework like Hardhat or Foundry?", question_type=QuestionType.SHORT_ANSWER, order_index=9, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: compile contracts, run tests, deploy to networks, debug, manage dependencies, local development environment.", is_active=True),
        Assessment(module_id=13, question_text="Describe how a front-end application communicates with a smart contract on the blockchain.", question_type=QuestionType.SHORT_ANSWER, order_index=10, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: JavaScript library (Ethers.js/Web3.js), RPC provider, contract ABI, wallet connection, transaction signing, reading state, writing transactions.", is_active=True),
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
        Assessment(module_id=14, question_text="True or False: All ERC-20 tokens must implement the same set of required functions.", question_type=QuestionType.TRUE_FALSE, order_index=5, points=10,
            options=None, correct_answer="True", explanation="The ERC-20 standard defines required functions (transfer, approve, balanceOf, etc.) that all compliant tokens must implement.", is_active=True),
        Assessment(module_id=14, question_text="True or False: You can create an ERC-20 token without writing any code.", question_type=QuestionType.TRUE_FALSE, order_index=6, points=10,
            options=None, correct_answer="False", explanation="Creating an ERC-20 token requires writing and deploying a smart contract, though templates and tools can simplify the process.", is_active=True),
        Assessment(module_id=14, question_text="True or False: ICOs are regulated the same way in all countries.", question_type=QuestionType.TRUE_FALSE, order_index=7, points=10,
            options=None, correct_answer="False", explanation="ICO regulations vary significantly by country. Some countries have strict regulations, while others have none. Always check local laws.", is_active=True),
        Assessment(module_id=14, question_text="Explain the key functions that an ERC-20 token contract must implement.", question_type=QuestionType.SHORT_ANSWER, order_index=8, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: transfer, approve, transferFrom, balanceOf, totalSupply, allowance, and events (Transfer, Approval).", is_active=True),
        Assessment(module_id=14, question_text="What are the main components of an ICO smart contract?", question_type=QuestionType.SHORT_ANSWER, order_index=9, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: token contract, sale parameters (price, cap, duration), contribution tracking, refund mechanism, token distribution.", is_active=True),
        Assessment(module_id=14, question_text="Describe the security considerations when creating and launching an ERC-20 token.", question_type=QuestionType.SHORT_ANSWER, order_index=10, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: code audits, access controls, overflow protection, re-entrancy guards, proper testing, secure deployment practices.", is_active=True),
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
        Assessment(module_id=15, question_text="True or False: NFT images are stored directly on the blockchain.", question_type=QuestionType.TRUE_FALSE, order_index=5, points=10,
            options=None, correct_answer="False", explanation="NFT images are typically stored on IPFS or other decentralized storage. Only the metadata (with IPFS hash) is stored on-chain due to gas costs.", is_active=True),
        Assessment(module_id=15, question_text="True or False: You can create an NFT marketplace without writing smart contracts.", question_type=QuestionType.TRUE_FALSE, order_index=6, points=10,
            options=None, correct_answer="False", explanation="An NFT marketplace requires smart contracts for listing, buying, and selling functionality, though you can use existing standards and contracts.", is_active=True),
        Assessment(module_id=15, question_text="True or False: All NFTs in a collection must have the same metadata.", question_type=QuestionType.TRUE_FALSE, order_index=7, points=10,
            options=None, correct_answer="False", explanation="Each NFT in a collection can have unique metadata (different images, names, attributes) while sharing the same contract.", is_active=True),
        Assessment(module_id=15, question_text="Explain why IPFS is used for storing NFT metadata instead of storing everything on-chain.", question_type=QuestionType.SHORT_ANSWER, order_index=8, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: gas costs, blockchain storage is expensive, IPFS is decentralized and permanent, content-addressed storage, cost-effective.", is_active=True),
        Assessment(module_id=15, question_text="What are the main functions needed in an NFT marketplace smart contract?", question_type=QuestionType.SHORT_ANSWER, order_index=9, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: listNFT, buyNFT, cancelListing, setPrice, handle payments, transfer ownership, fee collection.", is_active=True),
        Assessment(module_id=15, question_text="Describe the process of creating and deploying an NFT collection.", question_type=QuestionType.SHORT_ANSWER, order_index=10, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: design images, generate metadata, upload to IPFS, write ERC-721 contract, deploy contract, mint NFTs, verify on explorer.", is_active=True),
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
        Assessment(module_id=16, question_text="True or False: Building a simple blockchain helps you understand how real blockchains work.", question_type=QuestionType.TRUE_FALSE, order_index=5, points=10,
            options=None, correct_answer="True", explanation="Creating a simple blockchain implementation teaches the core concepts: blocks, hashing, chaining, and consensus mechanisms.", is_active=True),
        Assessment(module_id=16, question_text="True or False: Mining profitability depends only on the price of cryptocurrency.", question_type=QuestionType.TRUE_FALSE, order_index=6, points=10,
            options=None, correct_answer="False", explanation="Mining profitability depends on multiple factors: hardware costs, electricity costs, cryptocurrency price, network difficulty, and block rewards.", is_active=True),
        Assessment(module_id=16, question_text="True or False: All blockchains use the same consensus mechanism.", question_type=QuestionType.TRUE_FALSE, order_index=7, points=10,
            options=None, correct_answer="False", explanation="Different blockchains use different consensus mechanisms: Proof-of-Work, Proof-of-Stake, DPoS, PoA, and others.", is_active=True),
        Assessment(module_id=16, question_text="Explain how blocks are cryptographically linked together in a blockchain.", question_type=QuestionType.SHORT_ANSWER, order_index=8, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: each block contains hash of previous block, creates chain, any change breaks hash chain, immutability.", is_active=True),
        Assessment(module_id=16, question_text="What factors determine mining profitability and how would you calculate it?", question_type=QuestionType.SHORT_ANSWER, order_index=9, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: hash rate, electricity cost, hardware cost, block reward, network difficulty, price of cryptocurrency, pool fees.", is_active=True),
        Assessment(module_id=16, question_text="Describe the basic steps to build a simple blockchain from scratch.", question_type=QuestionType.SHORT_ANSWER, order_index=10, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: define block structure, implement hashing, create genesis block, add blocks with previous hash, implement basic consensus, validate chain.", is_active=True),
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
        Assessment(module_id=17, question_text="True or False: AI trading bots guarantee profits.", question_type=QuestionType.TRUE_FALSE, order_index=5, points=10,
            options=None, correct_answer="False", explanation="No trading system guarantees profits. Markets are unpredictable, and all trading involves risk of loss.", is_active=True),
        Assessment(module_id=17, question_text="True or False: Multi-source data integration improves decision-making in AI agents.", question_type=QuestionType.TRUE_FALSE, order_index=6, points=10,
            options=None, correct_answer="True", explanation="Combining multiple data sources (price data, social sentiment, on-chain metrics) provides more comprehensive information for better decisions.", is_active=True),
        Assessment(module_id=17, question_text="True or False: Risk management is optional in trading bot development.", question_type=QuestionType.TRUE_FALSE, order_index=7, points=10,
            options=None, correct_answer="False", explanation="Risk management is critical. Without proper risk controls (stop losses, position sizing, limits), bots can lose significant capital quickly.", is_active=True),
        Assessment(module_id=17, question_text="Explain why it's important to integrate multiple data sources in an AI trading agent.", question_type=QuestionType.SHORT_ANSWER, order_index=8, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: comprehensive view, reduce bias, confirm signals, better decisions, market context, cross-validation.", is_active=True),
        Assessment(module_id=17, question_text="What are technical indicators and how are they used in trading bots?", question_type=QuestionType.SHORT_ANSWER, order_index=9, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: mathematical calculations on price/volume, identify trends, signals, examples (RSI, MACD, moving averages), automated analysis.", is_active=True),
        Assessment(module_id=17, question_text="Describe the key components of a well-designed AI trading bot architecture.", question_type=QuestionType.SHORT_ANSWER, order_index=10, points=10,
            options=None, correct_answer="", explanation="Instructor will review. Key points: data gathering, analysis engine, decision logic, risk management, execution system, monitoring, logging, error handling.", is_active=True),
    ]


