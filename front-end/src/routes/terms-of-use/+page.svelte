<script lang="ts">
	import Header from '$lib/components/layout/Header.svelte';
	import Footer from '$lib/components/layout/Footer.svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<svelte:head>
	<title>Terms of Use | SG Lib Books</title>
</svelte:head>
<Header user={data.user} />
<main class="container p-8">
	<h1 class="text-4xl font-bold text-slate-700 mb-6">Terms of Use</h1>
	<h2 class="text-xl font-semibold text-slate-700">2.1 Service Overview</h2>
	<p class="mb-3">
		Our web app is offered as an open-source project, free of charge, and provided "as is."
	</p>

	<h2 class="text-xl font-semibold text-slate-700">2.2 Acceptable Use</h2>
	<ul class="list-disc pl-4 mb-3">
		<li>Use the service only for lawful purposes.</li>
		<li>Respect the privacy and rights of other users.</li>
	</ul>

	<h2 class="text-xl font-semibold text-slate-700">2.3 Limitation of Liability</h2>
	<p class="mb-3">
		We make no guarantees about the service's availability or functionality. We are not responsible
		for data loss, service interruptions, or any damages arising from using the app.
	</p>

	<h2 class="text-xl font-semibold text-slate-700">2.4 Intellectual Property</h2>
	<p class="mb-3">
		The source code is licensed under MIT License. All contributions are governed by the same
		license. Content, trademarks, and other intellectual property related to the project remain the
		property of their respective owners.
	</p>

	<h2 class="text-xl font-semibold text-slate-700">2.5 Termination</h2>
	<p class="mb-3">
		We reserve the right to suspend or terminate access to the service for violations of these
		terms.
	</p>

	<h2 class="text-xl font-semibold text-slate-700">2.6 Disclaimer</h2>
	<p class="mb-3">
		The service is provided "as is" without any warranties, express or implied. We disclaim all
		liability for damages arising from its use.
	</p>

	<h2 class="text-xl font-semibold text-slate-700">2.7 Governing Law</h2>
	<p class="mb-3">
		These terms are governed by the laws of the Republic of Singapore. Any disputes arising from the
		use of the service will be resolved under the exclusive jurisdiction of the courts of Singapore.
	</p>

	<h2 class="text-xl font-semibold text-slate-700">2.8 Exclusion of Liability</h2>
	<p class="mb-3">
		To the fullest extent permitted by Singapore law, we disclaim all liability for any indirect,
		incidental, or consequential damages arising from your use of the app, including data loss,
		service interruptions, or technical failures.
	</p>

	<h2 class="text-xl font-semibold text-slate-700">2.9 Account Responsibility</h2>
	<p class="mb-3">
		Users are responsible for maintaining the confidentiality of their login credentials. Any
		activity conducted under their account is their responsibility.
	</p>

	<h2 class="text-xl font-semibold text-slate-700">2.10 Modification of Terms</h2>
	<p class="mb-3">
		We reserve the right to modify these terms at any time. Users will be notified of significant
		changes via the app or email.
	</p>

	<h2 class="text-xl font-semibold text-slate-700">2.11 External Links</h2>
	<p class="mb-3">
		The app may contain links to third-party websites. We are not responsible for the content or
		privacy policies of these external sites.
	</p>

	<h2 class="text-xl font-semibold text-slate-700">2.12 Indemnification</h2>
	<p class="mb-3">
		Users agree to indemnify and hold the developers harmless from claims, damages, or expenses
		arising from their use of the app.
	</p>

	<h2 class="text-xl font-semibold text-slate-700">2.13 Force Majeure</h2>
	<p class="mb-3">
		We are not liable for service interruptions caused by events beyond our control, such as natural
		disasters, cyberattacks, or government restrictions.
	</p>

	<h2 class="text-xl font-semibold text-slate-700">Contact Us</h2>
	<p class="mb-3">
		For any questions regarding this <a href="/privacy-statement" class="underline"
			>Privacy Statement</a
		>
		and <a href="/terms-of-use" class="underline">Terms of Use</a>, please contact us at
		<a href="mailto:sglibreads@gmail.com" class="underline">sglibreads@gmail.com</a>.
	</p>
</main>
<Footer />
