create type "public"."NotificationType" as enum ('all_notif', 'book_updates_only', 'no_notif');

alter table "public"."users" drop column "HashedPassword";

alter table "public"."users" drop column "books_updated";

alter table "public"."users" drop column "latest_login";

alter table "public"."users" drop column "preferred_lib";

alter table "public"."users" drop column "pw_ans";

alter table "public"."users" drop column "pw_qn";

alter table "public"."users" drop column "registered_time";

alter table "public"."users" add column "channel_email" boolean not null default true;

alter table "public"."users" add column "channel_push" boolean not null default true;

alter table "public"."users" add column "notification_type" "NotificationType" not null default 'all_notif'::"NotificationType";

set check_function_bodies = off;

CREATE OR REPLACE FUNCTION public.handle_new_user()
 RETURNS trigger
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO ''
AS $function$begin
  insert into public.users ("UserName", "email_address")
  VALUES (
  	new.email,
  	new.raw_user_meta_data ->> 'name'
	) ON CONFLICT DO NOTHING;
  return new;
end;$function$
;

