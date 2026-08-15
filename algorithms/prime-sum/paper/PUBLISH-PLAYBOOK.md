# The complete publishing playbook — step by step, in order

Everything below is sequenced. Don't reorder: the DOI must exist before the
email, and the email before the social posts.

---

## YOUR IDENTITY — use this everywhere, consistently

One public research identity, across every platform below:
- Name: **Raghav Sharma**
- Email: **raghavsharma1729@gmail.com** (never any other address)
- LinkedIn: https://www.linkedin.com/in/raghav-sharma-a66023179/
- New GitHub account (Step 0), ORCID, Zenodo, Overleaf, arXiv, Medium:
  ALL registered with raghavsharma1729@gmail.com. Consistency is what lets
  professors, arXiv endorsement, and citations connect back to one person.

## STEP 0 — A separate GitHub account for research (recommended; ~15 min)

Since your existing GitHub account carries your startup and other projects,
a dedicated research account is the right call — it is common practice and
keeps the two identities cleanly apart.

1. Log out of GitHub (or use a private browser window).
2. github.com → Sign up → email raghavsharma1729@gmail.com → username
   suggestion: `raghavsharma-math` (or similar — professional and clearly
   research-flavoured).
3. On the new account: New repository → name `weighted-prime-races` →
   **Public** → leave ALL checkboxes unchecked → Create repository.
4. Upload the prepared content — no git required:
   - Unzip `weighted-prime-races-upload.zip` (Claude prepared it: clean
     code + papers + MIT LICENSE + landing README, wrong-email-free).
   - On the empty repo page click "uploading an existing file".
   - Drag ALL unzipped files/folders into the upload box, commit message
     "Weighted prime races and analytic prime sums", click Commit.
5. Your public research repo now exists under the research account with a
   commit authored by it. Copy its URL for the steps below.

Note on Claude access: this session's GitHub connection is bound to your
original account, so Claude cannot push to the new account from here. If
you want Claude working on the new account in future sessions, connect it
at claude.ai → Settings → integrations (install the GitHub app while logged
into the NEW account). Not needed for launch — the drag-and-drop above
covers everything.

## STEP 1 — Compile the paper to PDF (10 min)

1. overleaf.com → register (free) → New Project → Upload Project →
   upload `weighted-races.tex` (zip it first if the uploader requires a zip).
2. Click Recompile → Download PDF. Name it `weighted-races.pdf`.
3. Read the PDF once, fully. You are about to put your name on it.

## STEP 2 — Zenodo: the timestamp + DOI (20 min)

Zenodo is run by CERN, free, permanent, and gives you a DOI instantly —
this is your priority protection.

1. zenodo.org → Sign up (you can log in with your GitHub account).
2. Click "New upload".
3. Files: drag in `weighted-races.pdf` AND `prime-sum-research.tar.gz`.
4. Fill the form:
   - Resource type: **Preprint**
   - Title: `Rubinstein–Sarnak densities for weighted prime number races`
   - Creators: Raghav Sharma (make a free ORCID at orcid.org first with
     raghavsharma1729@gmail.com — 5 min; journals and arXiv want it)
   - Description: paste the paper's abstract, then add one line:
     "All code and data included. Work produced with substantial AI
     assistance (Anthropic's Claude); every result independently verified —
     see the paper's disclosure."
   - License: **Creative Commons Attribution 4.0** (CC-BY-4.0)
   - Related works (optional): your GitHub repo URL, relation "is supplemented
     by".
5. Click **Publish**. You now have a DOI like `10.5281/zenodo.XXXXXXX`.
   That timestamp is your proof of priority, forever.
6. (Optional polish) Add the DOI line to the .tex title footnote, recompile,
   and upload the updated PDF as version 2 on Zenodo — same DOI family.

## STEP 3 — The email to Prof. Martin (15 min)

1. Open `outreach-email.md`. Replace `[link to repository]` with BOTH links:
   the Zenodo DOI (https://doi.org/10.5281/zenodo.XXXXXXX) and the GitHub URL.
2. Add this sentence at the end of the second-to-last paragraph:
   "If you find the note credible, I would also be grateful for an arXiv
   endorsement for math.NT, so it can reach the community properly."
3. Attach `weighted-races.pdf`. Send to **gerg@math.ubc.ca**.
4. Do NOT email five professors the same day with the same text. One primary
   (Martin). Wait ~2 weeks. Then, if silence: Prof. Koyama via the contact
   form at researchmap.jp/koyama (he posed Problem 12), with the same content
   lightly rephrased. Then, if silence: any analytic number theorist at a
   university near you, using the local-professor template below.

### Template B — local/nearby professor (for mentorship, not priority)

Subject: Student seeking guidance on a number theory preprint

Dear Professor [NAME],

I am a student working independently on computational analytic number
theory. With substantial AI assistance (fully disclosed in the draft), I
have computed what appear to be the first Rubinstein–Sarnak densities for
weighted prime number races, addressing Problem 12 of the comparative prime
number theory problem list (arXiv:2407.03530). The preprint, code, and data
are public: [DOI LINK].

I am looking for guidance on making the error analysis rigorous and on
publication. Would you have 20 minutes to advise me, or could you point me
to a colleague or graduate student who might?

Thank you for your time,
Raghav Sharma
raghavsharma1729@gmail.com

## STEP 4 — LinkedIn + Medium (same day or day after the email)

1. Publish the Medium article (`medium-article.md`) — replace both link
   placeholders first.
2. Post the LinkedIn post (`linkedin-post.md`) from your profile
   (linkedin.com/in/raghav-sharma-a66023179) — follow its tagging rules:
   no tagging researchers you haven't interacted with.
3. Optionally link the Medium article as a comment under your LinkedIn post
   (LinkedIn suppresses posts with external links in the body).

## STEP 5 — arXiv (when endorsement arrives)

1. arxiv.org → create account with a real email.
2. Register with raghavsharma1729@gmail.com. Submit to **math.NT**. First-time submitters need an
   endorsement: the submission page gives you an endorsement code to send to
   an endorser (this is the ask already added to the Martin email).
3. Upload the .tex source (arXiv compiles it), abstract, and in Comments:
   "Code and data: [DOI]".
4. Once live, add the arXiv number everywhere (Zenodo metadata, Medium,
   LinkedIn, repo README).

## STEP 6 — What happens next: the four scenarios

- **He replies with interest** → answer within 24h, offer everything openly,
  say yes to a call. If collaboration is offered: that's the jackpot — a
  rigorous joint version in a journal beats a solo preprint by miles.
- **He replies with corrections** → thank him, fix, push, update Zenodo
  (new version), reply with the fixes. Corrections from Greg Martin are a
  gift, not a setback.
- **Silence (most likely — it's normal)** → follow-up after 2 weeks (3 polite
  lines max), then move down the ladder in Step 3.4. Your DOI protects you
  the entire time.
- **Someone publishes δ(m) independently later** → your Zenodo timestamp
  predates them; polite email pointing to it, and standard practice is they
  cite you. This is exactly what the DOI is for.

## Timeline reality check

| thing | time |
|---|---|
| Zenodo DOI | minutes |
| Email reply | days–weeks (possibly never; normal) |
| arXiv live (after endorsement) | 2–3 days |
| Journal, submission → decision | 6–18 months |
| Journal, acceptance → print | +6–12 months |

The DOI is your protection; the journal is a stamp that arrives later.
Nobody in mathematics waits for the journal to consider work "out."

## Rules that protect you (read twice)

1. Never claim more than the paper claims. The paper's phrasing survived an
   adversarial audit; improvised phrasing on social media might not.
2. AI involvement is stated everywhere, always, unprompted. It is a strength
   in this story; concealment would be the only scandal.
3. Results are conditional on GRH + LI — same as the whole field's — say it
   when asked, without embarrassment.
4. Respond to every substantive correction within a day, gratefully. Speed
   and grace on corrections is how unknown researchers build reputations.
5. One professor at a time. Mass-emailing is spam and they compare notes.
