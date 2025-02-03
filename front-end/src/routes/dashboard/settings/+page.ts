import { superValidate } from "sveltekit-superforms";
import { zod } from "sveltekit-superforms/adapters";
import { readUser } from '$lib/api/user'
import { profileFormSchema } from "$lib/components/forms/user-settings.svelte";
import type { PageLoad } from "./$types.js";

export const load: PageLoad = async ({ parent }) => {
	const { client } = await parent();
	const data = await readUser(client)
	const form = await superValidate(data, zod(profileFormSchema))

	return { form };
};

