<script lang="ts">
	import Header from '$lib/components/layout/Header.svelte';
	import Footer from '$lib/components/layout/Footer.svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<svelte:head>
	<title>Privacy Statement | SG Lib Books</title>
</svelte:head>
<Header user={data.user} />
<main class="container p-8">
	<h1 class="text-4xl font-bold text-slate-700 mb-6">Privacy Statement</h1>

	<h2 class="text-xl font-semibold text-slate-700">1.1 Who We Are</h2>
	<p class="mb-3">
		We are a group of independent engineers contributing to an open-source project. We are not
		affiliated with any company or organization.
	</p>

	<h2 class="text-xl font-semibold text-slate-700">1.2 Data We Collect</h2>
	<ul class="list-disc pl-4 mb-3">
		<li><strong>Email Address:</strong> Required for account creation and authentication.</li>
		<li>
			<strong>Usage Data:</strong> May include non-identifiable data such as app interactions to improve
			functionality.
		</li>
	</ul>

	<h2 class="text-xl font-semibold text-slate-700">1.3 How We Use Your Data</h2>
	<ul class="mb-3">
		<li>To provide access to the app.</li>
		<li>To improve the app's performance.</li>
		<li>We do not sell or share your personally identifiable information with third parties.</li>
	</ul>

	<h2 class="text-xl font-semibold text-slate-700">1.4 Data Security</h2>
	<p class="mb-3">
		We use reasonable measures to protect your data. However, since this is a community-driven
		open-source project, we cannot guarantee full data security.
	</p>

	<h2 class="text-xl font-semibold text-slate-700">1.5 Third-Party Services</h2>
	<p class="mb-3">
		We may use third-party APIs to provide certain functionalities. Please review their respective
		privacy policies.
	</p>

	<h2 class="text-xl font-semibold text-slate-700">1.6 Your Rights</h2>
	<p class="mb-3">
		You can request data deletion or modification by contacting us at <a
			href="mailto:sglibreads@gmail.com"
			class="underline">sglibreads@gmail.com</a
		>.
	</p>

	<h2 class="text-xl font-semibold text-slate-700">1.7 Policy Updates</h2>
	<p class="mb-3">We may update this policy occasionally. Changes will be posted on this page.</p>

	<h2 class="text-xl font-semibold text-slate-700">1.8 Legal Basis for Data Processing</h2>
	<p class="mb-3">
		We collect and process personal data in accordance with Singapore's Personal Data Protection Act
		(PDPA). By using the app, you consent to the collection, use, and processing of your data as
		outlined in this policy.
	</p>

	<h2 class="text-xl font-semibold text-slate-700">1.9 Data Retention</h2>
	<p class="mb-3">
		We will retain personal data for as long as necessary to provide the service or as required by
		law. If you request account deletion, your personal data will be removed unless retention is
		required by legal obligations.
	</p>

	<h2 class="text-xl font-semibold text-slate-700">1.10 User Consent and Opt-Out</h2>
	<p class="mb-3">
		By using our service, you consent to the collection and processing of your data. You may
		withdraw consent at any time by contacting us at <a
			href="mailto:sglibreads@gmail.com"
			class="underline">sglibreads@gmail.com</a
		>, though this may limit your access to our service.
	</p>

	<h2 class="text-xl font-semibold text-slate-700">1.11 Cookies and Tracking Technologies</h2>
	<p class="mb-3">
		We may use cookies or similar technologies to enhance your user experience. You can adjust your
		browser settings to manage cookies, though certain features may not function properly without
		them.
	</p>

	<h2 class="text-xl font-semibold text-slate-700">1.12 Data Breach Notification</h2>
	<p class="mb-3">
		In the unlikely event of a data breach affecting personal information, we will notify affected
		users and relevant authorities as required by Singapore law.
	</p>
</main>
<Footer />
