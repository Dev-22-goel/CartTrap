# Gemini 4 NYC Hackathon: Rules and Guide

## Problem Statements

### Problem Statement One: 5 Sigma

Most hackathon agents work in the demo and nowhere else. Pick a real task that today's agents struggle with, and build a Gemini 4 system that does it reliably, using the appropriate models for the task at hand. Then prove it: build an evaluation that tests your system on inputs you didn't prepare for, and show how it compares to a simple baseline.

Questions to answer:
- What's your baseline (a single model call, an existing tool, or the way people do it today), and how much better does your system do?
- How do you build a test set that reflects real use, including messy inputs and edge cases, rather than the happy path?
- Where does your system still fail, and what did you change after seeing those failures?

Examples:
- An agent that fills out messy real-world forms (scanned PDFs, handwritten notes), tested on 50 documents it has never seen, with an accuracy score against a single-model baseline.
- A coding agent that fixes real GitHub issues, measured on how many fixes pass the repo's own tests.

### Problem Statement Two: Element 119

Build something that only works because Gemini 4 can see, hear and generate media. Video, audio, images or documents should be the core input, and they can be the output too. Use any Gemini 4 models you want plus the [Decisions API](https://aistudio.google.com/docs/changelog?e=0#11-11-2026), and push them as far as they go: longer footage, messier audio, more streams at once, faster real-time loops. Then show us where it breaks.

Questions to answer:
- What's the hardest input you can throw at it, and does it still hold up?
- What does your project get from the raw video, audio or images that a text description would lose?
- How far did you push before it broke, and what did you change to get past that point?

Not allowed:
- Text-only chatbots
- Demos that only run on scripted inputs
- Evaluations made up entirely of examples the team wrote to pass

### Bonus Track: Build with Commerce (Shopify)

Use [shop.dev](https://shop.dev) to build a commerce experience, from product discovery to a shopping agent, for a chance to win an additional prize. Open to all builders.

## Rules

- **Open source:** repositories must be public.
- **Team size:** 1-4 team members per team.
- **Demo requirements:** your demo must only highlight the specific features, code, and functionality that your team built during the hackathon. Judges must be able to clearly identify what was created during the event. Failure to clearly identify your original contributions will result in immediate disqualification.
- **New work only:** you may not present an existing project as your own work. Failure to clearly distinguish your contributions will result in immediate disqualification.
- **Banned projects:** projects will be disqualified if they:
  - violate legal, ethical, or platform policies
  - use code, data, or assets you do not have the rights to

## Anti-Projects (Strictly NO)

- AI Mental Health Advisor
- Basic RAG Applications
- Streamlit Applications
- Image Analyzers
- "AI for Education" Chatbot
- AI Job Application Screener
- AI Nutrition Coach
- Personality Analyzers
- Any project using AI to generate and give medical advice
- Any project where a dashboard is the main feature
- Sports analyzers or coaches

## Partner Resources

### Shopify
Build commerce experiences on [shop.dev](https://shop.dev), from product discovery to shopping agents.

- **Builder docs:** [shop.dev](https://shop.dev)
- **Support:** Shopify Solutions Engineers will be online during the event to answer questions in the Discord.

### Google DeepMind and other partners
Coming soon (not yet published in the guide).
