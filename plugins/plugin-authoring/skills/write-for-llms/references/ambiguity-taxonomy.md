# Ambiguity Taxonomy

Self-audit framework based on Berry-Kamsties-Krieger classification. Use to identify and fix ambiguities in LLM-consumed documents.

## The Four Types

| Type | Definition | Detection Question |
|------|------------|-------------------|
| **Lexical** | Same word, multiple meanings | "Could this word mean something else?" |
| **Syntactic** | Structure permits multiple parses | "Could this sentence be parsed differently?" |
| **Semantic** | Reference or scope unclear | "What exactly does this refer to?" |
| **Pragmatic** | Meaning depends on unstated context | "What am I assuming the reader knows?" |

---

## Type 1: Lexical Ambiguity

The same word has multiple dictionary meanings.

### Examples

| Ambiguous | Meanings | Resolution |
|-----------|----------|------------|
| "Check the **bank**" | Financial institution / riverside | Use domain-specific term or define on first use |
| "**Table** the discussion" | US: postpone / UK: bring forward | Avoid idioms; use literal "postpone" or "begin now" |
| "Process the **record**" | Database row / audio file / documentation | "Process the database row" |
| "**Execute** the script" | Run code / sign document | "Run the script" |

### Fix Pattern

1. Identify words with multiple meanings in your domain
2. Choose one meaning per word for entire document
3. Define in glossary if ambiguity risk is high
4. Use domain-specific alternatives where available

### Common Offenders in Technical Prose

| Word | Potential Meanings |
|------|-------------------|
| Object | Programming object / physical thing / goal |
| Class | OOP class / category / CSS class |
| Type | Data type / to keyboard / kind |
| Port | Network port / hardware port / to migrate |
| Branch | Git branch / conditional branch / tree branch |
| Instance | Object instance / example / occurrence |

---

## Type 2: Syntactic Ambiguity

Sentence structure allows multiple valid parses.

### Modifier Attachment

**Ambiguous:** "Old men and women"  
**Parses:**  
- [Old men] and [women] (old applies to men only)  
- [Old] [men and women] (old applies to both)

**Ambiguous:** "The system processes valid requests and responses"  
**Parses:**  
- The system processes [valid requests] and [responses]  
- The system processes [valid requests and responses]

**Fix:** Restructure to force single parse.
- "Old men and old women" (applies to both)
- "Women and old men" (applies to men only)
- "Valid requests and valid responses" (applies to both)

### Coordination Scope

**Ambiguous:** "Read and write files or directories"  
**Parses:**  
- [Read and write files] or [directories]
- [Read] and [write files or directories]
- [Read and write] [files or directories]

**Fix:** Use explicit grouping.
- "Read files, write files, or access directories"
- "Perform read or write operations on files and directories"

### Prepositional Phrase Attachment

**Ambiguous:** "Send the report to the manager with the charts"  
**Parses:**  
- Send [the report with the charts] to [the manager]
- Send [the report] to [the manager with the charts]

**Fix:** Restructure.
- "Send the chart-containing report to the manager"
- "Send the report to the manager who requested charts"

---

## Type 3: Semantic Ambiguity

Words are clear, structure is clear, but meaning is still ambiguous.

### Referential Ambiguity

**Ambiguous:** "The parser reads the config. It validates the schema."  
**Question:** What does "it" refer to—parser or config?

**Ambiguous:** "After the service processes the request, return the result to the caller."  
**Question:** Who returns—the service or the calling code?

**Fix:** Repeat nouns; eliminate pronouns in cross-sentence references.
- "The parser reads the config. The parser validates the schema."

### Quantifier Scope

**Ambiguous:** "Every user can edit some documents."  
**Parses:**  
- Each user can edit certain documents (different docs per user)
- There exist some documents that every user can edit (same docs for all)

**Fix:** State scope explicitly.
- "Each user can edit documents assigned to them"
- "All users can edit the shared document pool"

### Collective vs. Distributive

**Ambiguous:** "The team members wrote the report."  
**Parses:**  
- Together (one report, collaborative)
- Each (multiple reports, one per member)

**Fix:** Specify collective or distributive.
- "The team members collaborated on one report"
- "Each team member wrote their own report"

---

## Type 4: Pragmatic Ambiguity

Meaning depends on context, conventions, or implied knowledge.

### Presupposition

**Ambiguous:** "Stop sending notifications after business hours."  
**Presupposes:** Reader knows what business hours are.

**Fix:** Define or eliminate presupposition.
- "Stop sending notifications between 18:00 and 09:00 UTC"
- "Stop sending notifications outside configured business hours (default: 09:00-18:00 local time)"

### Implicature

**Ambiguous:** "The system is performant."  
**Implies:** System meets performance requirements.  
**But:** What requirements? Whose definition of performant?

**Fix:** Replace implied standards with explicit criteria.
- "The system responds within 200ms for 95th percentile requests"

### Speech Act Ambiguity

**Ambiguous:** "You should validate input."  
**Could be:** Strong recommendation / mandatory requirement / optional best practice

**Fix:** Use explicit modality.
- "Validate input" (imperative = mandatory)
- "Input validation is required" (explicit requirement)
- "Consider validating input for untrusted sources" (explicit recommendation)

---

## Quick Audit Checklist

Run through each question for your document:

### Lexical
- [ ] Any word used in multiple senses throughout document?
- [ ] Any word that has domain-specific meaning not defined?
- [ ] Any idioms or figures of speech?

### Syntactic
- [ ] Any modifier that could attach to multiple elements?
- [ ] Any coordination (and/or) with unclear scope?
- [ ] Any prepositional phrase with ambiguous attachment?

### Semantic
- [ ] Any pronoun without clear, unambiguous antecedent?
- [ ] Any quantifier (all, some, every) with unclear scope?
- [ ] Any collective noun that could be distributive or vice versa?

### Pragmatic
- [ ] Any presupposed knowledge not stated in document?
- [ ] Any implied standard not made explicit?
- [ ] Any recommendations that could be read as requirements (or vice versa)?

---

## Extended Classification

Beyond the core four types, additional ambiguity patterns appear in technical documents:

| Type | Example | Fix |
|------|---------|-----|
| **Elliptical** | "Validate input; output too" (validate output?) | Complete the ellipsis: "Validate input; validate output too" |
| **Scopal** | "Don't log all errors" (log none? log some?) | "Log errors selectively" or "Log no errors" |
| **Vagueness** | "Recent updates" (how recent?) | "Updates from the past 24 hours" |
| **Generality** | "Use appropriate formatting" | Define what constitutes appropriate |

---

## Resolution Priority

When multiple ambiguities exist, resolve in this order:

1. **Lexical** — Foundational; other fixes may fail if terms are unclear
2. **Semantic** — References must be clear before structure matters
3. **Syntactic** — Restructure for single valid parse
4. **Pragmatic** — Eliminate implicit assumptions last
