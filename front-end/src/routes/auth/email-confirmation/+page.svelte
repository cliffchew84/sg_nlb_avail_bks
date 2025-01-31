<script lang="ts">
	import { goto } from '$app/navigation';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
	if (data.session) {
		// Redirect to dashboard if user is already logged in
		goto('/dashboard');
	}
</script>

<svelte:head>
	<title>Email Confirmation | SG Lib Books</title>
</svelte:head>

<div class="flex flex-col space-y-2 text-center">
	<h1 class="text-2xl font-semibold tracking-tight">Email Confirmation</h1>
	<p class="text-muted-foreground text-sm">
		A confirmation email has been sent to your inbox. Follow the link provided in it to login.
	</p>
</div>
