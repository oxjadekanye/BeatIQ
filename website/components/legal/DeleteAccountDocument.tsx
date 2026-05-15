import { company } from "@/lib/site";

const deletionMailto =
  "mailto:admin@beatiq.co.uk?subject=BeatIQ%20Account%20Deletion%20Request";

export function DeleteAccountDocument() {
  return (
    <article className="prose-article mx-auto max-w-3xl px-4 pb-16 pt-8 sm:px-6 lg:px-8">
      <h1>Delete Your BeatIQ Account</h1>
      <p className="effective">Last updated: 15 May 2026</p>

      <p>
        BeatIQ users can request deletion of their account and associated personal data. This
        page explains how to submit a request and what happens after we receive it.
      </p>

      <h2>Who operates BeatIQ</h2>
      <p>
        BeatIQ is a product of <strong className="text-zinc-100">{company.name}</strong>, located
        at {company.lines.join(", ")}.
      </p>

      <h2>How to request account deletion</h2>
      <p>
        Email{" "}
        <a href={`mailto:${company.email}`} className="text-beatiq-accent hover:underline">
          {company.email}
        </a>{" "}
        using the <strong className="text-zinc-100">same email address</strong> registered in the
        BeatIQ app.
      </p>
      <p>
        Use this subject line:{" "}
        <strong className="text-zinc-100">BeatIQ Account Deletion Request</strong>.
      </p>
      <p>
        In your message, you may include your registered email and any details that help us
        verify your account. We may ask for additional verification if needed to protect your
        account from unauthorised deletion requests.
      </p>

      <div className="not-prose mt-8">
        <a
          href={deletionMailto}
          className="inline-flex items-center justify-center rounded-full bg-violet-600 px-8 py-3 text-center text-sm font-semibold text-white shadow-lg shadow-violet-900/40 transition hover:bg-violet-500"
        >
          Email Account Deletion Request
        </a>
      </div>

      <h2>What we delete</h2>
      <p>
        After receiving a verified deletion request, BeatIQ will delete the user account and
        associated personal data within <strong className="text-zinc-100">7 days</strong>, unless
        retention is required for legal, fraud prevention, or security obligations.
      </p>
      <p>
        We will delete the user account and associated personal data unless retention is required
        by law, fraud prevention, security, or other legal obligations.
      </p>

      <h2>Data we may retain</h2>
      <p>
        Some non-personal technical logs may be retained for security and audit purposes for a
        limited period. This may include aggregated or de-identified information that cannot
        reasonably be used to identify you.
      </p>

      <h2>Contact</h2>
      <p>
        For questions about account deletion or your personal data, contact{" "}
        <a href={`mailto:${company.email}`} className="text-beatiq-accent hover:underline">
          {company.email}
        </a>
        .
      </p>
    </article>
  );
}
