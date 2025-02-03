alter table "public"."notifications" rename column "UserName" TO "email";

alter table "public"."user_books" rename column "UserName" TO "email";

alter table "public"."user_libraries" rename column "UserName" TO "email";

alter table "public"."user_search" rename column "UserName" TO "email";

alter table "public"."user_status" rename column "UserName" TO "email";

alter table "public"."users" rename column "UserName" TO "email";

alter table "public"."users" rename column "email_address" TO "username";

CREATE OR REPLACE FUNCTION public.handle_new_user()
 RETURNS trigger
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO ''
AS $function$begin
  insert into public.users ("email", "username")
  VALUES (
  	new.email,
  	new.raw_user_meta_data ->> 'name'
	) ON CONFLICT DO NOTHING;
  return new;
end;$function$
;

