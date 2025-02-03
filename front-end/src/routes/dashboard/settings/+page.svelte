<script lang="ts">
	import { cubicInOut } from 'svelte/easing';
	import { crossfade } from 'svelte/transition';
	import TitledPage from '$lib/components/layout/TitledPage.svelte';
	import Button from '$lib/components/ui/button/button.svelte';
	import UserSettingForm from '$lib/components/forms/user-settings.svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
	const items = ['Profile', 'Notifications'];
	let selected = $state(items[0]);

	const [send, receive] = crossfade({
		duration: 250,
		easing: cubicInOut
	});
</script>

<svelte:head>
	<title>Settings | SG Lib Books</title>
</svelte:head>

<TitledPage title="Settings" description="Manage your account settings and set e-mail preferences.">
	<div class="flex flex-col space-y-8 lg:flex-row lg:space-x-12 lg:space-y-0">
		<aside class="-mx-4 lg:w-1/5">
			<nav class="flex space-x-2 lg:flex-col lg:space-x-0 lg:space-y-1">
				{#each items as item}
					{@const isActive = selected === item}

					<Button
						on:click={() => (selected = item)}
						variant="ghost"
						class="relative justify-start hover:bg-transparent {!isActive && 'hover:underline'}"
						data-sveltekit-noscroll
					>
						{#if isActive}
							<div
								class="bg-muted absolute inset-0 rounded-md"
								in:send={{ key: 'active-sidebar-tab' }}
								out:receive={{ key: 'active-sidebar-tab' }}
							></div>
						{/if}
						<div class="relative">
							{item}
						</div>
					</Button>
				{/each}
			</nav>
		</aside>
		<UserSettingForm form={data.form} {selected} client={data.client} supabase={data.supabase} />
	</div>
</TitledPage>
