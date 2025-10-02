  MANDATORY: Before any code search, analysis, or debugging - ALWAYS check DocDNA first.

  SEARCH ORDER:
  1. **Config Section** - Check feature flags, constants, enabled functionality
  2. **Error/Exception Patterns** - Search for error messages, exception handling
  3. **Core Module Functions** - Main implementation files and key function signatures
  4. **Integration Points** - Where components connect and data flows
  5. **GUI/Interface** - User-facing elements and their backend connections

  SEARCH STRATEGY:
  - Use keyword search for: function names, error messages, feature names, file paths
  - Look for function signatures and class definitions first
  - Follow the data/call flow through the documented structure
  - Identify the PRIMARY file containing the functionality before examining actual code

  DEBUGGING APPROACH:
  - Search error message text in DocDNA first
  - Find exception handling patterns and their locations
  - Trace error propagation through the documented call stack
  - Identify logging/debug output locations

  CRITICAL RULE:
  DocDNA is your INDEX - it tells you WHERE to look in the actual codebase. Never guess file locations or assume implementation details. The DocDNA mapping prevents time-wasting searches through irrelevant files.

  EXAMPLE: "Find pause functionality" → Config shows ENABLE_INLINE_PAUSES → Core shows parse_pause_tags in tts.py → Integration shows generate() method usage → Then examine actual tts.py code.
