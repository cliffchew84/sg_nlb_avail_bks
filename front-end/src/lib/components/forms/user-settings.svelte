<script lang="ts" module>
	import { z } from 'zod';

	export const profileFormSchema = z.object({
		username: z
			.string()
			.min(2, 'Username must be at least 2 characters.')
			.max(30, 'Username must not be longer than 30 characters')
			.optional(),
		email: z.string({ required_error: 'Please select an email to display' }).email(),
		notification_type: z.enum(['all_notif', 'book_updates_only', 'no_notif']),
		channel_push: z.boolean().default(true),
		channel_email: z.boolean().default(true)
	});
	export type ProfileFormSchema = typeof profileFormSchema;
</script>

<script lang="ts">
	// import SuperDebug from 'sveltekit-superforms';
	import {
		type Infer,
		type SuperValidated,
		superForm,
		setMessage,
		type SuperForm,
		setError
	} from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import LoaderCircle from 'lucide-svelte/icons/loader-circle';

	import type { SupabaseClient } from '@supabase/supabase-js';
	import type BackendAPIClient from '$lib/api/client';
	import { updateUser } from '$lib/api/user';
	import * as Form from '$lib/components/ui/form/index.js';
	import * as RadioGroup from '$lib/components/ui/radio-group';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Switch } from '$lib/components/ui/switch/index.js';

	let data: {
		form: SuperValidated<Infer<ProfileFormSchema>>;
		selected: String;
		client: BackendAPIClient;
		supabase: SupabaseClient;
	} = $props();
	let form: SuperForm<Infer<ProfileFormSchema>> | undefined = $state();
	let {
		form: formData,
		enhance,
		submitting,
		message,
		errors
	} = (form = superForm(data.form, {
		SPA: true,
		resetForm: false,
		validators: zodClient(profileFormSchema),
		async onUpdate({ form }) {
			if (!form.valid) return;
			try {
				await updateUser(data.client, form.data);
				const { data: res, error } = await data.supabase.auth.updateUser({
					data: { name: form.data.username }
				});
				setMessage(form, 'Profile updated.');
			} catch (error) {
				setMessage(form, 'Error updating profile. Please try again.');
			}
		}
	}));
	let selected = $derived(data.selected);
</script>

<div class="w-full">
	<!-- <SuperDebug data={$formData} /> -->
	<form class="" method="POST" use:enhance>
		<div class="space-y-8 {selected == 'Profile' ? '' : 'hidden'}">
			<div>
				<h3 class="text-lg font-medium">Profile</h3>
				<p class="text-muted-foreground text-sm">This is how others will see you on the site.</p>
			</div>
			<Form.Field {form} name="username">
				<Form.Control let:attrs>
					<Form.Label>Username</Form.Label>
					<Input placeholder="Username" {...attrs} bind:value={$formData.username} />
				</Form.Control>
				<Form.Description>
					This is your public display name. It can be your real name or a pseudonym.
				</Form.Description>
				<Form.FieldErrors />
			</Form.Field>

			<Form.Field {form} name="email">
				<Form.Control let:attrs>
					<Form.Label>Email</Form.Label>
					<Input placeholder="@shadcn" {...attrs} bind:value={$formData.email} disabled />
				</Form.Control>
				<Form.Description>
					Your email address is used for account recovery and notifications. Please <a
						href="mailto:sglibreads@gmail.com"
						class="underline">contact us</a
					> if you need to change it.
				</Form.Description>
				<Form.FieldErrors />
			</Form.Field>
		</div>
		<div class="space-y-8 {selected == 'Notifications' ? '' : 'hidden'}">
			<div>
				<h3 class="text-lg font-medium">Notifications</h3>
				<p class="text-muted-foreground text-sm">Configure how you receive notifications.</p>
			</div>

			<Form.Fieldset {form} name="notification_type">
				<Form.Legend>Notify me about...</Form.Legend>
				<Form.Control>
					<RadioGroup.Root bind:value={$formData.notification_type}>
						<div class="flex items-center space-x-3">
							<Form.Control let:attrs>
								<RadioGroup.Item value="all_notif" {...attrs} />
								<Form.Label>New features, book updates and more.</Form.Label>
							</Form.Control>
						</div>
						<div class="flex items-center space-x-3">
							<Form.Control let:attrs>
								<RadioGroup.Item value="book_updates_only" {...attrs} />
								<Form.Label>Your book related activity only.</Form.Label>
							</Form.Control>
						</div>
						<div class="flex items-center space-x-3">
							<Form.Control let:attrs>
								<RadioGroup.Item value="no_notif" {...attrs} />
								<Form.Label>Nothing</Form.Label>
							</Form.Control>
						</div>
						<RadioGroup.Input name="type" />
					</RadioGroup.Root>
				</Form.Control>
			</Form.Fieldset>
			<div>
				<h3 class="mb-4 text-lg font-medium">Email Notifications</h3>
				<div class="space-y-4">
					<Form.Field
						{form}
						name="channel_push"
						class="flex flex-row items-center justify-between rounded-lg border p-4"
					>
						<Form.Control let:attrs>
							<div class="space-y-0.5">
								<Form.Label class="text-base">Push Notifications</Form.Label>
								<Form.Description>Receive push notification on your application.</Form.Description>
							</div>
							<Switch includeInput {...attrs} bind:checked={$formData.channel_push} />
						</Form.Control>
					</Form.Field>
					<Form.Field
						{form}
						name="channel_email"
						class="flex flex-row items-center justify-between rounded-lg border p-4"
					>
						<Form.Control let:attrs>
							<div class="space-y-0.5">
								<Form.Label class="text-base">Email Notifications</Form.Label>
								<Form.Description>Receive emails.</Form.Description>
							</div>
							<Switch includeInput {...attrs} bind:checked={$formData.channel_email} />
						</Form.Control>
					</Form.Field>
				</div>
			</div>
		</div>

		<Form.Button class="my-8">Save Changes</Form.Button>
	</form>
	{#if $submitting}
		<div class="flex justify-center items-center">
			<LoaderCircle class="m-8 h-6 w-6 animate-spin" />
		</div>
	{/if}
	{#if $message}<h3>{$message}</h3>{/if}
</div>
