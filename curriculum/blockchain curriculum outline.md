# Blockchain & Cryptocurrency Curriculum

**GitHub Repository:** https://github.com/TCoder920/crypto-curriculum

---

# How to Use This Curriculum

## Using AI as Your Learning Assistant

Throughout this curriculum, you are **strongly encouraged** to use AI tools as learning assistants to enhance your understanding:

### Recommended AI Tools
- **ChatGPT** (OpenAI) - https://chat.openai.com
- **Google Gemini** - https://gemini.google.com
- **Claude** (Anthropic) - https://claude.ai

### When to Use AI Tools

**✅ DO Use AI For:**
- Explaining concepts you don't understand in simpler terms
- Getting immediate answers to clarifying questions
- Generating additional examples or analogies
- Breaking down complex topics into smaller pieces
- Checking your understanding with practice questions
- Debugging code errors
- Exploring related topics mentioned in lessons

**❌ DON'T Use AI For:**
- Copying answers to assessments without understanding
- Replacing the curriculum content entirely
- Making trading decisions without your own research
- Trusting financial advice blindly
- Avoiding the learning process

### How to Ask Effective Questions

**Poor Question:**
> "What is blockchain?"

**Better Question:**
> "I'm learning about blockchain and the curriculum says it's a 'distributed ledger.' Can you explain what 'distributed' means in this context and give me a real-world analogy?"

**Best Question:**
> "I'm studying Module 1 of a blockchain curriculum. The lesson explains that Proof-of-Work uses mining and Proof-of-Stake uses validators, but I don't understand WHY Proof-of-Stake is more energy efficient. Can you explain the energy difference in simple terms, like I'm explaining it to a friend?"

### Example Prompts for Learning

**Understanding Concepts:**
- "Can you explain [concept] using a different analogy than [curriculum's analogy]?"
- "What's the difference between [concept A] and [concept B]?"
- "I don't understand this part: [paste confusing section]. Can you break it down?"

**Practice and Testing:**
- "Quiz me on [topic] with 5 questions"
- "Is my understanding correct? [explain what you think you learned]"
- "Give me a real-world scenario where I would use [concept]"

**Code Help (Developer Track):**
- "I'm getting this error: [error message]. What does it mean?"
- "Can you explain what this Solidity code does line by line: [paste code]"
- "How would I modify this code to [your goal]?"

### Important Boundaries

⚠️ **Remember:**
- AI tools can make mistakes or provide outdated information
- Always verify technical information with official documentation
- For financial decisions, consult multiple sources and professionals
- AI is a learning aid, not a replacement for understanding
- The curriculum is designed to build foundational knowledge - don't skip ahead

### Collaborative Learning

For the technical portions (Parts 3 & 4), you'll be encouraged to:
- Share your code with classmates for review
- Collaborate on projects and debugging
- Discuss different approaches to problems
- Learn from each other's implementations

---

# Part 1: The "User" Track (Foundations)

*Goal: To create an informed, safe, and competent user of Web3.*

## Module 1: Blockchain Technology
- **What is a Ledger?** Defining a centralized ledger (e.g., a bank) vs. a decentralized one.
- **Distributed Ledger Technology (DLT):** A database shared and synchronized across a network.
- **Immutability:** How records are final and cannot be altered.
- **Consensus Mechanisms:**
    - **Proof-of-Work (PoW):** "Miners" compete to solve a puzzle (e.g., Bitcoin). **Pros:** security, **Cons:** energy.
    - **Proof-of-Stake (PoS):** "Validators" lock coins as collateral to be chosen (e.g., Ethereum). **Pros:** efficiency, **Cons:** rich get richer.
    - DPoS (Delegated) and PoA (Authority).
- **Smart Contracts:** "If-This-Then-That" programs that run on the blockchain. *Analogy: A digital vending machine.*

## Module 2: Web3 Wallets & Security
- **Public Key vs. Private Key:** *Analogy: Public key is your email address; private key is your password.*
- **Types of Wallets:**
    - **Custodial:** A third party holds your keys (e.g., an exchange). **Pros:** easy, **Cons:** "Not your keys, not your coins".
    - **Non-Custodial:** You control your keys.
        - **Hot Wallets:** Software/browser wallets (e.g., MetaMask).
        - **Cold Wallets:** Hardware wallets (e.g., Ledger, Trezor).
- **The Seed Phrase (Secret Recovery Phrase):** The master key to restore a wallet.
- **Security Best Practices:** How to store a seed phrase (offline), bookmarking sites, avoiding public Wi-Fi.
- **Scams & Fraud-Prevention:**
    - Phishing, social engineering, malicious contracts.
    - Recognizing common scams (giveaways, fake airdrops, rug pulls).
    - Understanding "token approvals."

## Module 3: Transactions, dApps & Gas Fees
- **Anatomy of a Transaction:** From, To, Amount, and Data.
- **The "Mempool":** Where transactions wait to be processed.
- **Gas Fees:** The fee paid to validators/miners to process a transaction.
    - *Analogy: A processing fee or "postage stamp."*
    - How it's calculated (Supply & Demand).
- **dApps (Decentralized Applications):** Applications that run on the blockchain.
- **Layer-2 Scaling:**
    - **The Problem:** Layer-1s are slow and expensive.
    - **The Solution:** L2s (Rollups, Sidechains). *Analogy: A carpool lane for transactions.*

## Module 4: Tokens & Digital Assets
> NOTE: DIFFERENCE BETWEEN A COIN AND A TOKEN…

- **Tokenomics:** The economics of a token (supply, demand, minting, burning).
- **Token Types:** Utility tokens (access) vs. Governance tokens (voting).
- **Token Standards:**
    - **Ethereum (ERC):** ERC-20 (Fungible), ERC-721 (NFT), ERC-1155 (Hybrid).
    - **Solana (SPL):** A single, flexible program for all token types.
    - **Cardano (Native Assets):** Tokens handled directly by the ledger, not smart contracts.
    - **Bitcoin (BRC-20 & Ordinals):** Experimental standards for creating tokens and NFTs on Bitcoin.
- **Stablecoins:** Tokens pegged 1:1 to a fiat currency (e.g., USDC, USDT).
- **NFTs (Non-Fungible Tokens):**
    - What you own (the token/receipt, not the image).
    - Metadata: The data linked to the token.
    - Use cases beyond art (gaming, ticketing).

## Module 5: Trading
- **Centralized Exchanges (CEXs):**
    - **Definition:** Private companies (e.g., Coinbase, Binance, Kraken).
    - **Pros:** Fast, easy, fiat on-ramps.
    - **Cons:** Custodial, require KYC (Know Your Customer).
- **Decentralized Exchanges (DEXs):**
    - **Definition:** Smart contracts for peer-to-peer swaps (e.g., Uniswap).
    - **Pros:** Non-custodial, no KYC.
    - **Cons:** Gas fees, risk of impermanent loss.
- **Order Types:** Market Order (buy now) vs. Limit Order (buy at a set price).
- **Charting:** TradingView
- **Risk Management:** "Don't invest more than you can afford to lose," dangers of FOMO and FUD.

## Module 6: DeFi & DAOs
- **Decentralized Finance (DeFi):** Rebuilding traditional finance.
- **Lending & Borrowing:** Using collateral to get a loan.
- **Liquidity Pools (LPs):** "Pots" of two tokens that allow for swaps.
- **Yield Farming:** Providing liquidity to earn rewards.
- **Impermanent Loss:** The risk of providing liquidity.
- **Decentralized Autonomous Organizations (DAOs):**
    - **Definition:** "Internet-native" organizations run by code and a community.
    - **How they work:** Governance tokens for voting, proposals, and community treasuries.

## Module 7: Advanced Concepts Overview
- **Privacy:**
    - Pseudonymity (not anonymity) of blockchains.
    - **Mixers:** Tools to obscure transaction trails.
    - **Zero-Knowledge Proofs (ZKPs):** Proving something is true without revealing the "how" or "why."
- **Cross-Chain Interoperability:**
    - **The Problem:** Blockchains cannot talk to each other.
    - **The Solution:** Bridges and "Wrapped Tokens" (e.g., WBTC).
- **Mining (PoW Deep Dive):**
    - Hardware (ASICs vs. GPUs).
    - Profitability (hardware cost, electricity, crypto price).
    - The energy debate.

# Part 2: The "Power User" / Analyst Track

*Goal: To bridge the gap from using the chain to analyzing it.*

## Module 8: Practical On-Chain Analysis
- **Deep Dive: Block Explorers:** Reading smart contracts (Read/Write tabs), tracing wallet histories, identifying whale activity, analyzing token holders.
- **Wallet Tagging & Tracing:** Using tools (e.g., Etherscan, Arkham) to follow the flow of funds from exchanges, hackers, or major funds.
- **Protocol Analysis:** Using analytics dashboards (e.g., Dune Analytics, Nansen) to understand a protocol's health (Total Value Locked (TVL), user growth, revenue).

## Module 9: Advanced Market & Tokenomic Analysis
- **Technical Analysis (TA) Basics:** Reading candlestick charts, support/resistance, moving averages, Relative Strength Index (RSI).
- **Fundamental Analysis (FA) / "Crypto-Native" FA:** How to read a whitepaper, evaluate a project's team and backers, analyze token distribution/vesting schedules, and assess community engagement.
- **On-Chain Metrics:** Using on-chain data (e.g., hash rate, active addresses, network value to transaction ratio) to gauge market sentiment.

## Module 10: Advanced DeFi Strategies
- **Complex Yield Farming:** Leveraged yield farming, delta-neutral strategies, liquid staking derivatives.
- **DeFi Derivatives:** Introduction to decentralized perpetuals, options, and synthetics.
- **Protocol Risk Assessment:** How to identify smart contract risk, economic/oracle risk (e.g., de-pegging), and centralization risk.

# Part 3: The "Developer" Track (Prerequisites)

*Goal: To build the technical skills required to create smart contracts and dApps. This is a hard prerequisite for Part 4.*

## Module 11: Development & Programming Prerequisites
- **Programming Fundamentals:** Core computer science concepts (variables, functions, loops, data structures).
- **Web Development Basics:** How a website works (HTML, CSS, and JavaScript).
- **Development Tools Setup:** Installing a code editor (VS Code), Node.js, npm/yarn, and using a command-line terminal.

## Module 12: Smart Contract Development (Solidity & EVM)
- **Solidity Language:** Learning the core programming language of Ethereum (Data types, functions, modifiers, events, inheritance).
- **The Ethereum Virtual Machine (EVM):** Understanding the "computer" that runs the code.
- **Writing Contracts:** Building your first smart contracts (e.g., a simple storage contract, a basic token).
- **Smart Contract Security:** Learning to prevent common attacks (re-entrancy, overflows, front-running).

## Module 13: dApp Development & Tooling
- **Development Frameworks:** Using tools like Hardhat or Foundry to compile, test, and deploy contracts.
- **Front-End Integration:** Using JavaScript libraries (Ethers.js or Web3.js) to connect a website to a smart contract.
- **Building Your First dApp:** Creating a simple front-end (website) that can read data from and write data to your smart contract (e.g., a simple "guest book" or "mood setter").

# Part 4: The "Architect" / Builder Track (Application)

*Goal: To use the developer skills from Part 3 to build complex, novel systems.*

## Module 14: Creating a Fungible Token & ICO
- **Deep Dive: ERC-20:** A technical breakdown of the ERC-20 standard and its functions (e.g., transfer, approve, balanceOf).
- **Project: Launch Your Own Token:** Writing, testing, and deploying your own ERC-20 token contract.
- **Project: Building a "Launchpad":** Writing the smart contract for an Initial Coin Offering (ICO) or token sale.

## Module 15: Creating an NFT Collection & Marketplace
- **Deep Dive: ERC-721/1155:** A technical breakdown of NFT standards.
- **Metadata & IPFS:** Understanding how to host NFT images and metadata on decentralized storage.
- **Project: Launch Your Own NFT:** Writing, deploying, and managing the metadata for an NFT collection.
- **Project: Building a Simple Marketplace:** Writing the smart contracts to allow for listing, buying, and selling NFTs.

## Module 16: Building Your Own Blockchain & Mining
- **Blockchain Architecture:** Understanding the components (nodes, clients, networking, consensus) from a technical perspective.
- **Project: Build a Blockchain (Simple):** Creating a simple, functional blockchain in a language like Python or JavaScript to understand the concepts of blocks, chains, and hashes.
- **Mining/Validating Operations:** A technical look at setting up mining/validating hardware, joining a mining pool, and calculating profitability.

## Module 17: AI Agent Application Development

- **AI Agent Development Fundamentals**
- **Multi-Source Data Integration**
- **Social Media Sentiment Analysis (X/Twitter, Reddit, Discord, Telegram)**
- **AI Trading Bot Architecture**
- **Technical Indicators & Risk Management**
- **Multi-Source Decision Making**
- **Blockchain & DeFi Integration**
- **LLM-Agnostic Framework Implementation**
- **Backtesting & Performance Analytics**
- **Student Customization & Extension**

---

# Assessment Structure

**Each module includes 10 questions/tasks:**
- 3-4 Multiple choice questions
- 2-3 True/False questions with explanations
- 2-3 Short answer/definition questions
- 2-3 Practical tasks (where applicable)

**Total Assessments:** 170 questions/tasks across all 17 modules

**Format:**
- Questions test comprehension of core concepts
- Tasks test practical application of learned skills
- Auto-graded where possible (multiple choice, true/false)
- Manual review for short answers and practical tasks
- Minimum passing score: 70%

---

# Curriculum Summary

### Part 1: The "User" Track
Modules 1-7: Foundations of blockchain and Web3

### Part 2: The "Power User/Analyst" Track
Modules 8-10: On-chain analysis and advanced DeFi

### Part 3: The "Developer" Track
Modules 11-13: Smart contract and dApp development

### Part 4: The "Architect/Builder" Track
Modules 14-17: Building complex systems and AI applications

---

# Content Development Guidelines

**Each topic must include:**
1. Core Definition - Clear, simple explanation
2. Simple Analogies - Minimum 2 relatable analogies
3. Key Talking Points - Exhaustive itemized facts
4. Step-by-Step Process - How it works (if applicable)
5. Relevance/Importance - Why it matters and connections
6. Pros & Cons / Trade-offs - Balanced view
7. Common Misconceptions - What beginners get wrong
8. Critical Warnings - Security and financial risks (if applicable)

**Target Audience:** Complete beginners with no prior technical, financial, or blockchain knowledge.

### Additional Blockchain & Cryptocurrency Course Platforms

---

### COURSES ON COURSERA
* **Cost:** Courses can be audited for **free**. To earn certificates, pricing is per-course (approx. **$49-$99**), by Specialization (approx. **$49-$99/month**), or via Coursera Plus subscription (**$59/month** or **$399/year**).
* **Details:**
    * **Blockchain Specialization**
        * **Link:** `https://www.coursera.org/specializations/blockchain`
        * **Focus:** Fundamentals, consensus, smart contracts, and dApps. You design, code, deploy, and execute smart contracts in Solidity.
        * **Fit:** Modules 1, 3, 4, 12, 13.
    * **Smart Contracts**
        * **Link:** `https://www.coursera.org/learn/smarter-contracts`
        * **Focus:** Writing and deploying smart contracts, plus how contract logic encodes rules and policies.
        * **Fit:** Modules 12, 14.
    * **Decentralized Finance (DeFi) Specialization by Duke**
        * **Link:** `https://www.coursera.org/specializations/decentralized-finance-duke`
        * **Focus:** DeFi infrastructure, lending/borrowing, liquidity pools, automated market makers, MakerDAO, and protocol mechanics.
        * **Fit:** Modules 6, 9, 10.
    * **Blockchain, Cryptoassets, and Decentralized Finance**
        * **Link:** `https://www.coursera.org/learn/blockchain-crypto-decentralized-finance`
        * **Focus:** Transacting without intermediaries, cryptoasset economics, and distributed systems.
        * **Fit:** Modules 1, 2, 4, 5, 6.
    * **Solidity Mastery: Foundations to Advanced Smart Contracts**
        * **Link:** `https://www.coursera.org/specializations/packt-solidity-mastery-foundations-to-advanced-smart-contracts`
        * **Focus:** Solidity syntax, contract patterns, inheritance, security, testing, and deployment.
        * **Fit:** Modules 12, 13, 14, 15.

---

### COURSES ON BRILLIANT
* **Cost:** Requires a subscription (approx. **$24.99/month** or **$161.88/year**).
* **Details:**
    * **Cryptocurrency**
        * **Link:** `https://brilliant.org/courses/cryptocurrency/`
        * **Focus:** Math and mechanics behind cryptocurrencies. Covers cryptographic hashing, block linking, immutability, and Proof-of-Work.
        * **Fit:** Modules 1, 3, 7 (intro level).

---

### OTHER HIGH-FIT PLATFORMS

#### Udacity
* **Cost:** Per-program "Nanodegree" fee (approx. **$1,436** for the 4-month program).
* **Details:**
    * **Blockchain Developer Nanodegree**
        * **Link:** `https://www.udacity.com/course/blockchain-developer--nd1310`
        * **Focus:** Fundamentals, consensus, wallets; Solidity smart contract development, security; Hardhat testing; dApp building, including a collateralized loan contract.
        * **Fit:** Modules 1, 2, 3, 10, 11, 12, 13, 14, 15.

#### ConsenSys Academy
* **Cost:** Per-course fee. The mentor-led Bootcamp is approx. **$985**. The self-paced On-Demand track is approx. **$695**.
* **Details:**
    * **Blockchain Developer Bootcamp / Developer On-Demand**
        * **Link:** `https://consensys.io/academy`
        * **Focus:** End-to-end Ethereum development, Solidity, security, audits, and production deployment.
        * **Fit:** Modules 11, 12, 13, 14, 15.

#### Moralis Academy
* **Cost:** Subscription-based (Monthly and Yearly plans).
* **Details:**
    * **Example tracks:** Blockchain & Bitcoin 101, Ethereum Smart Contract Programming 101, DeFi 201.
        * **Link:** `https://academy.moralis.io`
        * **Focus:** Web3 developer school. Covers core concepts, Solidity, DeFi mechanics, and front-end integration.
        * **Fit:** Modules 1–5, 8–10, 11–13, 14–16.

#### MIT Sloan / GetSmarter
* **Cost:** Per-course fee (approx. **$3,500 - $3,850**).
* **Details:**
    * **Blockchain and Crypto Applications: From DeFi to Web3**
        * **Link:** `https://executive.mit.edu/course/blockchain-and-crypto-applications--from-decentralized-finance-to-web-3/a054v00000rHFLVAA4.html`
        * **Focus:** Economics of blockchain, stablecoins, NFTs, DeFi protocols, and Web3 business strategy.
        * **Fit:** Modules 8, 9, 10, 14, 15.

#### Alchemy University
* **Cost:** **Free**.
* **Details:**
    * **Ethereum Developer Bootcamp / Road to Web3**
        * **Link:** `https://www.alchemy.com/university/courses`
        * **Focus:** Comprehensive, free courses covering EVM development from fundamentals to advanced dApp and smart contract creation.
        * **Fit:** Modules 11-15.

#### CryptoZombies
* **Cost:** **Free**.
* **Details:**
    * **Gamified Solidity Tutorial**
        * **Link:** `https://cryptozombies.io/`
        * **Focus:** Interactive, game-based school that teaches Solidity programming by building a zombie game.
        * **Fit:** Modules 12, 15.

#### Chainalysis Academy
* **Cost:** Per-certification fee (approx. **$650** per course).
* **Details:**
    * **Certification Programs**
        * **Link:** `https://www.chainalysis.com/chainalysis-certification-programs/`
        * **Focus:** Professional training for on-chain analysis, transaction tracing, and wallet analysis.
        * **Fit:** Modules 8-10.

#### Udemy
* **Cost:** Per-course fee (prices vary, frequent sales).
* **Details:**
    * **Blockchain Topic Page:** `https://www.udemy.com/topic/blockchain/`
    * **Solidity Topic Page:** `https://www.udemy.com/topic/solidity/`
    * **Focus:** Wide variety of user- and developer-focused courses covering all topics.
    * **Fit:** All Parts (1-4).

#### edX
* **Cost:** Courses can be audited for **free**. To earn a verified certificate, the fee is approx. **$50 - $300** per course.
* **Details:**
    * **Blockchain Courses & Certificates**
        * **Link:** `https://www.edx.org/learn/blockchain`
        * **Focus:** University-level courses (e.g., from UC Berkeley, Linux Foundation) on blockchain fundamentals and developer tracks.
        * **Fit:** All Parts (1-4).

#### Web3 University
* **Cost:** **Free**.
* **Details:**
    * **Learning Tracks**
        * **Link:** `https://www.web3.university/`
        * **Focus:** A collection of free tutorials and learning paths for building dApps and NFT contracts.
        * **Fit:** Modules 11-15.

**Current as of:** November 2, 2025

