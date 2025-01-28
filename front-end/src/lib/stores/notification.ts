import { toast } from 'svelte-sonner';
import { writable } from 'svelte/store';

import type { Notification } from '$lib/models';
import type BackendAPIClient from '$lib/api/client';
import { getNotifications, readNotification } from '$lib/api/notification';

export const notificationStore = writable<Record<string, Notification>>({});

export async function fetchNotifications(client: BackendAPIClient) {
	try {
		const notifications = await getNotifications(client);
		notificationStore.set(
			notifications.reduce((acc, notif) => {
				acc[String(notif.id)] = {
					...notif,
					onClick: async () => {
						try {
							await readNotification(client, notif.id);
							notificationStore.update((s) => {
								s[String(notif.id)].isRead = true;
								return s;
							});
						} catch (error) {
							toast.warning('Failed to mark notification as read');
							console.error('Failed to mark notification as read', error);
						}
					}
				};
				return acc;
			}, {} as Record<string, Notification>)
		);
	} catch (error) {
		console.error('Failed to fetch notifications', error);
		throw error;
	}
}
