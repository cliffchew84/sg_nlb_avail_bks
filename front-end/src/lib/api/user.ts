
import type BackendAPIClient from './client';
import type { User, UserUpdate } from './models';

export async function readUser(client: BackendAPIClient): Promise<User> {
	try {
		const response = await client.get({ path: `/user` });

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}, detail: ${await response.text()}`, {
				cause: response.status
			});
		}

		const data: User = await response.json();
		return data;
	} catch (error) {
		if (error instanceof Error) {
			console.error('Error querying api:', error.message);
		} else {
			console.error('An unknown error occurred while querying API');
		}
		throw error;
	}
}

export async function updateUser(client: BackendAPIClient, userUpdate: UserUpdate): Promise<User> {
	try {
		const response = await client.put({ path: `/user`, body: userUpdate });

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}, detail: ${await response.text()}`, {
				cause: response.status
			});
		}

		const data: User = await response.json();
		return data;
	} catch (error) {
		if (error instanceof Error) {
			console.error('Error querying api:', error.message);
		} else {
			console.error('An unknown error occurred while querying API');
		}
		throw error;
	}
}

export async function deleteUser(client: BackendAPIClient): Promise<void> {
	try {
		const response = await client.delete({ path: `/user` });

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}, detail: ${await response.text()}`, {
				cause: response.status
			});
		}
	} catch (error) {
		if (error instanceof Error) {
			console.error('Error querying api:', error.message);
		} else {
			console.error('An unknown error occurred while querying API');
		}
		throw error;
	}
}
