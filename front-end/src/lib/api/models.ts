export interface User {
	email: string;
	username: string | undefined;
	channel_push: boolean;
	channel_email: boolean;
	notification_type: 'all_notif' | 'book_updates_only' | 'no_notif';
}

export interface UserUpdate {
	email: string;
	username?: string;
	channel_push?: boolean;
	channel_email?: boolean;
	notification_type?: 'all_notif' | 'book_updates_only' | 'no_notif';
}

export interface BookInfo {
	BID: number;
	TitleName?: string;
	Author?: string;
	PublishYear?: string;
	Publisher?: string;
	Subjects?: string;
	isbns?: string;
	cover_url?: string;
	summary?: string;
}

export interface BookAvail {
	ItemNo: string;
	CallNumber: string;
	BranchName: string;
	StatusDesc?: string;
	InsertTime?: number;
	BID: number;
	DueDate?: string;
	UpdateTime?: string;
}

export interface BookResponse extends BookInfo {
	avails: BookAvail[];
}

export interface Library {
	name: string;
	opening_status: string;
	start_hour?: string;
	end_hour?: string;
	opening_description?: string;
	address?: string;
	cover_url?: string;
}

export interface LibraryResponse extends Library {
	isFavourite: boolean;
}

export interface Notification {
	id: number;
	title: string;
	description?: string;
	createdAt: Date;
	action: string;
	isRead: boolean;
}
