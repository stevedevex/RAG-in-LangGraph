---
name: ai-augmentation-discovery
description: Reverse-engineer this repository, list everything it offers and everything a developer must know to work on it, and propose the GitHub Copilot customizations (instructions, prompts, skills, agents) that capture all of it under .github. Writes a report and a catalog only.
argument-hint: "focus=<area, optional> out=<output folder, optional>"
agent: agent
---

# AI augmentation discovery

You're reverse-engineering the repository open in this workspace. The goal: everything it offers, and everything a
developer needs to know to work on it, ends up captured in `.github` as GitHub Copilot customizations, so future work
with Copilot starts from complete and correct knowledge.

You produce two files:

- A **report**: what the repository is, everything it offers, the knowledge you can't see from a single file, and how
  people work in it, all backed by evidence.
- A **catalog**: the Copilot customizations to build, each justified by that evidence, with a coverage matrix showing
  that every offering, knowledge item and workflow is captured by at least one of them.

You don't build anything in this run. You never create or change `copilot-instructions.md`, `*.instructions.md`,
`*.prompt.md`, `SKILL.md` or `*.agent.md` files. You propose them in the catalog, and people decide what gets built.

The examples below are for Java, Maven and Spring Boot. If the repository uses something else, look for the
equivalents.

## Inputs

| Input         | Value                                                                      | If empty, or still shows a `${input:…}` placeholder              |
|---------------|----------------------------------------------------------------------------|------------------------------------------------------------------|
| Repository    | `${workspaceFolder}`                                                       | The folder open in this workspace                                |
| Focus         | `${input:focus:An area to go deeper on, e.g. soap, ssl, config, or blank}` | Cover every area at the same depth                               |
| Output folder | `${input:out:Folder for the report and catalog, or blank}`                 | `.github/ai-augmentation/<today, YYYY-MM-DD>/` in the repository |

A focus area gets more depth, but the inventory in step 2 still covers the whole repository.

## Ground rules

1. **Read only.** The two output files are the only files you write. No edits, commits, branch switches, stashes or
   dependency installs. Builds only as step 9 allows.
2. **Evidence for every finding.** Cite `path:line`, or the command you ran and what it showed. Mark every finding:
    - **Observed**: seen directly in code, configuration or history.
    - **Inferred**: a pattern across several examples. Give the count and the counter-examples.
    - **Unknown**: you couldn't tell. It becomes a question for the team.

   Never fill a gap from general knowledge of the frameworks, or from what a typical project would do.
3. **Code beats docs.** When docs, comments or existing guidance files disagree with the code, the code wins. Record
   the disagreement as a finding.
4. **No secrets, no client data, no people.** Name properties and files, never their values when they're passwords,
   tokens, keys, certificates, connection strings, tenant or client ids, or internal hostnames. Never copy payloads that
   hold client data. Write `<placeholder>` instead. From git history, report counts only: never names or email
   addresses.
5. **Copilot customization lives only under `.github`.** Nothing at the repository root (no `AGENTS.md`), nothing in IDE
   folders (`.idea`, `.vscode`).
6. **Know where the repository is hosted.** Check `git remote -v`. If it isn't GitHub (for example GitLab), no proposal
   may rely on the Copilot cloud coding agent or GitHub Actions.
7. **Say what you covered.** Record what you read in depth, what you sampled and what you skipped.

## Step 0: Preflight

- Record the repository path, the remote host, the branch (`git rev-parse --abbrev-ref HEAD`), the commit
  (`git rev-parse --short HEAD`), whether the working tree is clean (`git status --short`), and today's date.
- Record the tools available to an agent here: Java version, build tool and wrapper (`mvnw`), Docker, whether the
  artifact repository is reachable or only offline builds work. Agents can only use what exists.
- Find every existing piece of guidance, wherever it is: files under `.github/`, `SKILL.md` or agent files anywhere in
  the tree, README and `docs/`, decision records, contributing guides, merge request templates. They're inputs to
  evaluate, not things to replace. For guidance outside `.github`, note where its content should move.

## Step 1: Map the repository, breadth first

- **What it is:** a library, a set of starters, a service, an application. Confirm it from the code, not from its name.
- **Build:** build tool, root build file, parent, modules and their packaging, Java version, framework versions (from
  dependency management and properties), plugins (code generation, enforcer, formatting, coverage, test runners,
  release) and profiles.
- **Module graph:** draw the dependency graph between modules as a text tree, from the build files.
- **Dependencies:** the main third-party libraries and their versions, internal artifacts pulled from the company
  repository, exclusions and version overrides (each one usually hides a reason: find it), and how upgrades are done.
- **Size:** source files, rough lines of code and test classes per module.

## Step 2: Inventory everything the repository offers

This is the heart of the run. List **every** offering, each with an id (`O-01`, `O-02` …). An offering is anything a
developer can use, configure, extend or rely on. Look for:

- **Modules and artifacts:** what each module is for, and what a user adds to their build (starters, BOMs, modules).
- **Auto-configuration:** `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`,
  `spring.factories`, `@AutoConfiguration` and `@Configuration` classes, the beans they create, their
  `@ConditionalOn…` conditions and ordering.
- **Configuration properties:** every `@ConfigurationProperties` prefix, as a full property tree: name, type, default,
  where it's bound and where it's used. Note whether configuration metadata exists
  (`additional-spring-configuration-metadata.json`). Find any merge or precedence logic (for example defaults, then a
  named profile, then a per-item override) and the class that implements it.
- **Public APIs:** factories, registries, clients, templates, helpers and annotations meant to be called or used.
- **Extension points:** interfaces or base classes a user implements, and beans a user can override.
- **Integration types:** each protocol or integration (REST, SOAP, JDBC, messaging, vendor jars, whatever exists): how a
  new downstream or endpoint is declared, what is code and what is only configuration, and the interceptors or filters
  with their order or phase.
- **Contracts and data formats:** WSDLs, XSDs, OpenAPI files, JSON schemas, database or document shapes (e.g. MongoDB
  collections), and where each comes from (in the repo, or unpacked from another artifact).
- **Build-time behaviour:** code generation (e.g. `wsdl2java`, OpenAPI generators): its inputs, where the output goes,
  and whether it's committed.
- **Cross-cutting behaviour:** SSL and certificates, authentication and tokens (propagation, exchange, caching),
  correlation ids, logging and masking, timeouts and retries, caching, persistence, health, metrics and tracing.
- **Error model:** the exception hierarchy, error codes, and how downstream faults are mapped.
- **Test support:** test utilities, base classes, stubs and fixtures the repository provides.
- **Samples:** sample applications, example configuration, sample specs.
- **Compatibility:** how versions are published, deprecations (`@Deprecated`, `@DeprecatedConfigurationProperty`) and
  migration notes.

For each offering, record: what it does, how it's switched on and used (configuration, code or both), where it lives
(`path:line`), its tests, its docs, and its state: stable, deprecated, experimental, or incomplete (`TODO`, stubs,
missing tests).

**Prove the inventory is complete.** Count mechanically, and check that every counted item maps to an offering:

- modules in the build files;
- entries in every `AutoConfiguration.imports` and `spring.factories`;
- `@ConfigurationProperties` classes and their leaf properties;
- `@Bean` methods in auto-configuration classes;
- public types outside internal or implementation packages;
- interceptors, filters, and classes in test-support modules;
- contract files (WSDL, XSD, OpenAPI, schemas) and code generation executions.

Report the counts and list anything counted that isn't in the inventory.

## Step 3: Knowledge an agent can't see from one file

This is what agents most often get wrong, because it lives in people's heads, in docs, or across many files. List each
item with an id (`K-01`, `K-02` …).

- **Vocabulary:** domain terms and abbreviations used in class, package and property names. Give the meaning only when
  code, comments or docs state it; otherwise it's a question.
- **Design decisions:** each decision with its reason and any rejected alternative, from decision records, docs and
  comments. Agents must not undo a decision or bring back a rejected alternative.
- **Non-obvious behaviour:** things that look wrong but are intended (search comments for "because", "must", "don't",
  "never", "NOTE", "workaround"), ordering that matters (filters, interceptor phases, bean order, configuration
  precedence), thread-local context and its cleanup, blocking versus reactive calls, resource lifecycles, caching and
  expiry.
- **Security-sensitive areas:** where tokens, certificates, credentials and client data flow; where logging could leak
  them; which files or settings a change should get extra review for.
- **Compatibility rules:** what counts as a breaking change for the people who use this repository (renamed or removed
  properties, bean names, package moves, changed defaults), and how such changes are announced.
- **Known problems:** open `TODO` and `FIXME` items, documented limitations, and areas the history shows break often.

## Step 4: Conventions, measured

For each candidate rule, count the examples that follow it and the ones that don't. Candidates: constructor or field
injection, records or classes for configuration and DTOs, Lombok, null handling, logging style, exception handling,
package layout, class and test naming, Javadoc, method size, immutability, where generated sources go.

Also record the language level and which modern features the code actually uses (records, sealed types, pattern
matching, `var`, text blocks), so agents write code in the same style, and the formatting setup (`.editorconfig`,
formatter plugins).

**Module boundaries:** from the import statements, work out which modules use which libraries and packages (for
example, which modules import the SOAP stack, the HTTP client, the database driver or a cloud SDK). Report the
boundaries the code keeps, and every violation.

A rule is a candidate for instructions only when the code follows it consistently (about 90% or more) or a document
states it. Otherwise it's a **mixed practice**: report it, and add a question.

## Step 5: Tests

Test framework, assertion library, mocking, HTTP and SOAP stubbing (e.g. MockWebServer, WireMock), integration test
setup (Spring context slices, Testcontainers, embedded databases), test naming, where fixtures and sample responses live
and how they're made, how to run one module's tests or a single test class, slow or disabled tests, and any coverage
gates. Note which offerings have no tests. Pick 2–3 exemplar tests that show how testing is done here.

## Step 6: Running and debugging locally

- How to run the sample or application locally: profiles, required environment variables (names only), and the
  external systems it needs (databases, key vaults, downstream services), with how each can be stubbed or replaced.
- Local certificates or test credentials the setup expects (where they come from, never their values).
- Switches that help debugging: log levels, message or envelope logging, actuator endpoints.
- How a failing downstream call is traced: correlation ids, logs, error mapping.

If there's no way to run anything locally, say so: it limits what agents can verify.

## Step 7: Process and quality gates

- **CI:** the stages, what runs in each, and which failures block a merge.
- **Quality gates:** static analysis (e.g. Sonar, Checkstyle, SpotBugs, PMD, ArchUnit), enforcer rules, dependency and
  vulnerability scans, licence checks, coverage thresholds. Every gate is a rule agents must satisfy.
- **Merge requests:** templates, CODEOWNERS, required approvals visible in the repo, branch naming, and the commit
  message format (measure it from history: ticket keys, prefixes, tense).
- **Versions and releases:** versioning scheme (snapshots, semantic versioning), release steps, and how the changelog
  and migration notes are kept.
- **Ownership:** how many people change each module (counts only), and areas where one person makes most of the
  changes. Captured knowledge matters most there.

## Step 8: Change history: what people actually do

Recurring work shows what to automate. Adapt the period if the history is short or very busy.

- Commit subjects over the last 18 months (`git log --since=18.months --date=short --pretty=format:'%h %ad %s'`).
  Cluster them into change types: new integration or protocol, new property, dependency or framework upgrade,
  certificate or SSL change, bug fix by area, refactoring, tests only, docs, release.
- Hot files and modules (`git log --since=18.months --name-only --pretty=format: | sort | uniq -c | sort -rn`), and
  the largest, most complex classes. Files that are both large and often changed are where agents need the most help.
- Files that usually change together, for example a properties class with its metadata, docs and test. This is the
  **change recipe** for a change type.
- Reverts, and fixes that follow soon after a change in the same area: signs of where mistakes happen.

For each change type, give its frequency, its change recipe, and one example commit. If the history is too short to
show patterns, say so and derive the likely change types from the structure instead, marked Inferred.

## Step 9: Check the commands you'll recommend

Commands that would go into instructions (build everything, build one module, run one test class, regenerate sources,
run the static checks, start the sample): run the cheapest form of each once if it's safe and takes a few minutes at
most (offline, quiet, a single module). Record each as passed, failed or not run. Never run `install`, `deploy`, a
release, or anything that writes outside the build output folders.

## Step 10: Derive the capabilities

### 10.1 Workflows

From steps 2–8, list the developer workflows, each with an id (`W-01`, `W-02` …). Look for all of these kinds:

| Kind        | Examples                                                                                           |
|-------------|----------------------------------------------------------------------------------------------------|
| Understand  | Onboarding to the repo, explaining how an offering works, finding where something is done          |
| Use         | Configuring, calling or extending an offering correctly                                            |
| Change      | Adding an offering, changing one, adding a property, refactoring                                   |
| Upgrade     | Dependencies, the framework or Java version, contract versions (WSDL, OpenAPI)                     |
| Test        | Writing tests the way this repo does, creating stubs and fixtures                                  |
| Investigate | Tracing a failure, explaining a wrong value or a startup error                                     |
| Review      | Checking a merge request against the rules, boundaries, compatibility and security-sensitive areas |
| Document    | Keeping docs, the property reference and migration notes in step with the code                     |
| Release     | Version bump, changelog, migration notes                                                           |

For each workflow: what starts it, its steps today (the change recipe), the files it touches, how often it happens,
where it hurts or goes wrong (with evidence: reverts, fixes, mixed practices), and what a person must decide.

Also list what agents would need that doesn't exist yet: scripts (for example, generating the property reference or
checking module boundaries), templates and skeletons for recurring files, and access to outside systems (ticket
system, artifact repository, wiki). Outside systems usually mean an MCP server, which is registered in each person's
IDE, outside `.github`. Mark those as setup the team has to decide on.

### 10.2 Choose the building block

Pick the lightest block that does the job:

| Block             | Where                                                                            | Use it for                                                                                                                                                     | Not for                                                                                                            |
|-------------------|----------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|
| Repo instructions | `.github/copilot-instructions.md`                                                | What's true for almost every change: what the repo is, the module map, build and test commands, the non-negotiable rules                                       | Anything long, task-specific or only for some files. It's loaded into every chat, so keep it to one or two screens |
| Path instructions | `.github/instructions/<name>.instructions.md` with an `applyTo` glob             | Rules for a set of files: a module, configuration files, tests, build files, contract files                                                                    | Rules for every file, or rules needed only during one task                                                         |
| Prompt file       | `.github/prompts/<name>.prompt.md`                                               | A task a person starts on purpose, with a few inputs, done in one run: "add a downstream service", "add a property"                                            | Tasks that need a lot of reference material (skill) or a role with its own tools and loop (agent)                  |
| Skill             | `.github/skills/<name>/SKILL.md`, with scripts, templates and examples beside it | Know-how loaded only when relevant: the property reference, how an offering works and is used, the vocabulary, troubleshooting, an upgrade guide, test recipes | Short rules (instructions)                                                                                         |
| Custom agent      | `.github/agents/<name>.agent.md`                                                 | A role with its own tools, boundaries and loop (build until green, review against the rules), possibly handing off to other agents                             | Anything a single prompt can do                                                                                    |
| Subagent          | An agent another agent calls                                                     | A focused, context-heavy sub-task whose result comes back, e.g. "find every use of property X"                                                                 | Work that needs to talk to the user                                                                                |

How they fit together: instructions apply on their own; prompts and agents use skills for know-how; agents call
subagents. Keep each fact in one place and point to it, so nothing is said twice and goes out of step. Other Copilot
features (for example hooks) may be proposed only as options for the team to check against the Copilot version they
use.

### 10.3 Catalog entry format

```markdown
### C-07 <Name>

Type: skill · Captures: O-03, O-04, K-02, W-05

- **Purpose:** one sentence.
- **Trigger:** when it's used. For skills and agents, the description text that makes Copilot pick it.
- **Example requests:** 2–3 requests that should use it, and one similar request that shouldn't.
- **Draft frontmatter:** name, description, and `applyTo`, `argument-hint` or tools, as relevant.
- **Tools and permissions:** read only or editing; which commands it may run. Give it the least it needs.
- **Inputs → outputs.**
- **Encodes:** the knowledge and rules it carries, each with evidence (`path:line`).
- **Steps** (prompts and agents): a numbered outline.
- **Guardrails:** what it must never do, and what it hands back to a person to decide.
- **Verification:** how we'll know it works: a build, a test, a check.
- **Golden task:** a past commit that did this task, to replay later as a test (prompts and agents), if history has one.
- **Goes stale when:** the files or globs whose changes would make it wrong.
- **Value:** frequency, time saved and risk reduced, each Low, Medium or High, with the evidence.
- **Effort:** S, M or L. **Depends on:** other entries.
- **Confidence:** High, Medium or Low. **Open questions.**
```

### 10.4 Coverage matrix

A table with one row per offering (`O-…`), knowledge item (`K-…`) and workflow (`W-…`), and the catalog entries that
capture it. Every row needs at least one entry. If a row truly needs none, say why (for example, it's deprecated and due
for removal). Then check the other way: every catalog entry captures at least one row.

### 10.5 Keeping it current

Propose how the customizations stay true as the code changes: from each entry's "Goes stale when", which code changes
should trigger an update; a prompt or check that compares the customizations with the code; and who owns `.github`
(for example, a CODEOWNERS entry).

## Step 11: Write the outputs

`<output folder>/report.md`:

1. Header: repository, remote host, branch, commit, date, focus.
2. Summary: 10 bullets at most.
3. What the repository is, and the tools available to agents.
4. Build, modules and dependencies: the graph, and the commands with their check results.
5. The inventory of offerings (step 2), with the completeness counts.
6. Knowledge an agent can't see from one file (step 3).
7. Conventions with their counts, and mixed practices.
8. Tests, including offerings without tests.
9. Running and debugging locally.
10. Process and quality gates.
11. Change history: change types, change recipes, hot spots.
12. Existing guidance, how it compares with the code, and where its content should move under `.github`.
13. Risks and guardrails for agents: generated code, compatibility, secrets, security-sensitive areas, module
    boundaries.
14. Where docs and code disagree.
15. Questions for the team: every Unknown and mixed practice.
16. Coverage of this run: read in depth, sampled, skipped.

`<output folder>/catalog.md`:

1. Overview table: id, name, type, what it captures, value, effort, confidence.
2. The proposed `.github` tree.
3. An outline of `copilot-instructions.md` (headings and bullets only, within the size budget).
4. The entries, in the format of step 10.3, grouped by type: instructions, prompts, skills, agents and subagents.
5. The coverage matrix (step 10.4).
6. What agents need that doesn't exist yet: scripts, templates, access to outside systems.
7. Keeping it current (step 10.5).
8. Suggested build order: the 2–3 entries to build first, with the best value for the effort, each with its golden
   task.
9. Considered and rejected, and why.

## Step 12: Finish

In the chat, reply with a summary of five lines at most, the paths of both files, the number of offerings, knowledge
items and workflows found, any row left uncovered, the three entries to build first, and the number of open questions.
Don't create any other files.

## Working on a large repository

- Breadth before depth. Sample 3–5 examples of a pattern, and stop once it's clear. The inventory in step 2 is the
  exception: it must be complete.
- Search rather than reading whole files.
- If your context runs short, write what you have to the report, mark the unfinished sections, and continue. Never
  guess to fill a section.
