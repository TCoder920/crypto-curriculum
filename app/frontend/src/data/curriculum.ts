export type LearningTrack = {
  id: string
  title: string
  goal: string
  moduleRange: string
  modules: number[]
}

export type CurriculumModule = {
  id: number
  title: string
  summary: string
  focus: string[]
  trackId: string
}

export const learningTracks: LearningTrack[] = [
  {
    id: 'user',
    title: 'Part 1 · The "User" Track',
    goal: 'Create an informed, safe, and competent user of Web3.',
    moduleRange: 'Modules 1-7',
    modules: [1, 2, 3, 4, 5, 6, 7],
  },
  {
    id: 'analyst',
    title: 'Part 2 · The "Power User/Analyst" Track',
    goal: 'Bridge the gap from using the chain to analyzing it.',
    moduleRange: 'Modules 8-10',
    modules: [8, 9, 10],
  },
  {
    id: 'developer',
    title: 'Part 3 · The "Developer" Track',
    goal: 'Build the technical skills needed to create smart contracts and dApps.',
    moduleRange: 'Modules 11-13',
    modules: [11, 12, 13],
  },
  {
    id: 'architect',
    title: 'Part 4 · The "Architect/Builder" Track',
    goal: 'Use developer skills to build complex, novel blockchain systems.',
    moduleRange: 'Modules 14-17',
    modules: [14, 15, 16, 17],
  },
]

export const curriculumModules: CurriculumModule[] = [
  {
    id: 1,
    title: 'Blockchain Technology',
    summary:
      'Understand distributed ledgers, immutability, consensus mechanisms, and smart contracts.',
    focus: [
      'Centralized vs decentralized ledgers',
      'Proof-of-Work vs Proof-of-Stake trade-offs',
      'Smart contracts as on-chain automation',
    ],
    trackId: 'user',
  },
  {
    id: 2,
    title: 'Web3 Wallets & Security',
    summary:
      'Master wallet types, seed phrase security, and red flags for scams or phishing attempts.',
    focus: [
      'Custodial vs non-custodial wallets',
      'Hot vs cold storage best practices',
      'Common wallet attack vectors',
    ],
    trackId: 'user',
  },
  {
    id: 3,
    title: 'Transactions, dApps & Gas Fees',
    summary:
      'Break down transactions, mempools, gas economics, and how decentralized apps run.',
    focus: [
      'Transaction anatomy and data payloads',
      'Layer-2 scaling analogies',
      'Gas pricing and demand',
    ],
    trackId: 'user',
  },
  {
    id: 4,
    title: 'Tokens & Digital Assets',
    summary:
      'Explore tokenomics, major token standards, NFTs, and stablecoin mechanics.',
    focus: [
      'Utility vs governance tokens',
      'ERC-20/721/1155, SPL, Cardano assets',
      'Stablecoins and NFT metadata',
    ],
    trackId: 'user',
  },
  {
    id: 5,
    title: 'Trading',
    summary:
      'Compare centralized and decentralized exchanges, order types, charting, and risk controls.',
    focus: [
      'Market vs limit orders',
      'DEX pros/cons and impermanent loss',
      'Managing FOMO/FUD',
    ],
    trackId: 'user',
  },
  {
    id: 6,
    title: 'DeFi & DAOs',
    summary:
      'Dive into lending, liquidity pools, yield farming, and DAO governance structures.',
    focus: [
      'Collateralized lending basics',
      'Liquidity pool dynamics',
      'DAO proposals and treasury management',
    ],
    trackId: 'user',
  },
  {
    id: 7,
    title: 'Advanced Concepts Overview',
    summary:
      'Survey privacy tools, cross-chain interoperability, and the realities of mining.',
    focus: [
      'Zero-knowledge proofs and mixers',
      'Bridges and wrapped tokens',
      'PoW hardware and energy debates',
    ],
    trackId: 'user',
  },
  {
    id: 8,
    title: 'Practical On-Chain Analysis',
    summary:
      'Use explorers and analytics tools to trace wallets, contracts, and protocol health.',
    focus: [
      'Tracing whale activity on Etherscan',
      'Wallet tagging methodologies',
      'Dashboarding with Dune or Nansen',
    ],
    trackId: 'analyst',
  },
  {
    id: 9,
    title: 'Advanced Market & Tokenomic Analysis',
    summary:
      'Blend technical and fundamental analysis to evaluate crypto assets and networks.',
    focus: [
      'Chart patterns and indicators',
      'Token distribution & vesting reviews',
      'Hash rate and active-address metrics',
    ],
    trackId: 'analyst',
  },
  {
    id: 10,
    title: 'Advanced DeFi Strategies',
    summary:
      'Study leveraged yield farming, DeFi derivatives, and how to assess protocol risk.',
    focus: [
      'Liquid staking derivatives',
      'Perpetuals, options, synthetic assets',
      'Smart contract and oracle risk analysis',
    ],
    trackId: 'analyst',
  },
  {
    id: 11,
    title: 'Development & Programming Prerequisites',
    summary:
      'Review programming fundamentals, web basics, and tooling setup required for builders.',
    focus: [
      'Variables, loops, and data structures',
      'HTML/CSS/JS refresher',
      'CLI and Node.js tooling setup',
    ],
    trackId: 'developer',
  },
  {
    id: 12,
    title: 'Smart Contract Development (Solidity & EVM)',
    summary:
      'Learn Solidity syntax, the Ethereum Virtual Machine, and secure contract patterns.',
    focus: [
      'Solidity types, modifiers, events',
      'EVM execution model',
      'Security pitfalls like re-entrancy',
    ],
    trackId: 'developer',
  },
  {
    id: 13,
    title: 'dApp Development & Tooling',
    summary:
      'Use frameworks like Hardhat to build, test, and ship full-stack decentralized apps.',
    focus: [
      'Hardhat/Foundry workflows',
      'Ethers.js/Web3.js integrations',
      'Shipping a read/write dApp front end',
    ],
    trackId: 'developer',
  },
  {
    id: 14,
    title: 'Creating a Fungible Token & ICO',
    summary:
      'Implement ERC-20 tokens and launchpad mechanics for token sales.',
    focus: [
      'ERC-20 function breakdowns',
      'Deploying and testing your own token',
      'ICO/launchpad contract architecture',
    ],
    trackId: 'architect',
  },
  {
    id: 15,
    title: 'Creating an NFT Collection & Marketplace',
    summary:
      'Build ERC-721/1155 collections, manage metadata, and launch basic NFT marketplaces.',
    focus: [
      'Metadata + IPFS storage flows',
      'Minting and managing collections',
      'Marketplace contract logic',
    ],
    trackId: 'architect',
  },
  {
    id: 16,
    title: 'Building Your Own Blockchain & Mining',
    summary:
      'Explore blockchain architecture, craft a simple chain, and analyze mining operations.',
    focus: [
      'Node, consensus, and networking layers',
      'Hands-on mini blockchain project',
      'Mining hardware + profitability math',
    ],
    trackId: 'architect',
  },
  {
    id: 17,
    title: 'AI Agent Application Development',
    summary:
      'Combine AI, data pipelines, and crypto signals to design AI-first trading assistants.',
    focus: [
      'Multi-source data ingestion',
      'AI trading bot architecture',
      'Backtesting and performance analytics',
    ],
    trackId: 'architect',
  },
]

export const platformStats = [
  { label: 'Comprehensive Modules', value: '17' },
  { label: 'Assessment Questions', value: '170+' },
  { label: 'Learning Tracks', value: '4' },
  { label: 'Question Types', value: 'Multiple formats' },
]

export const assessmentStructure = {
  questionsPerModule: 10,
  totalQuestions: 170,
  passingScore: '70%',
  mix: [
    '3-4 Multiple choice questions',
    '2-3 True/False questions with explanations',
    '2-3 Short answer or definition prompts',
    '2-3 Practical tasks where applicable',
  ],
  notes: [
    'Questions test comprehension of core concepts.',
    'Practical tasks validate real-world application.',
    'Auto-graded where possible, manual review for written/practical work.',
  ],
}

export const aiAssistantGuidance = {
  recommendedTools: ['ChatGPT', 'Google Gemini', 'Claude'],
  do: [
    'Ask for simpler explanations and analogies when topics feel unclear.',
    'Use AI to break complex modules into actionable steps.',
    'Generate practice questions or debugging help during the developer track.',
    'Validate your understanding by explaining concepts back to the model.',
  ],
  dont: [
    'Copy assessment answers without understanding them.',
    'Use AI as a substitute for doing the coursework.',
    'Take financial advice at face value without additional research.',
    'Skip foundational modules because AI can generate summaries.',
  ],
  questionTips: [
    'Provide module context and what specifically confused you.',
    'Ask for comparisons, pros/cons, or real-world analogies.',
    'Share your current understanding and request validation.',
  ],
  promptExamples: {
    concept:
      '"I\'m in Module 1 learning about distributed ledgers. Can you explain how immutability works using a real-world analogy?"',
    comparison:
      '"Compare Proof-of-Work vs Proof-of-Stake using energy usage and security trade-offs."',
    debugging:
      '"My Solidity contract from Module 12 throws a re-entrancy error. Here is the snippet—why is it vulnerable and how can I fix it?"',
  },
}
