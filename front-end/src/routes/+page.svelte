<script lang="ts">
	import { LogIn, Library, Radar, Sprout, Smartphone, Linkedin, Github } from 'lucide-svelte';
	import Autoplay from 'embla-carousel-autoplay';

	import * as Carousel from '$lib/components/ui/carousel/index.js';
	import Header from '$lib/components/layout/Header.svelte';
	import Footer from '$lib/components/layout/Footer.svelte';
	import { Button } from '$lib/components/ui/button';
	import readingPic from '$lib/images/reading.gif';
	import bookPic from '$lib/images/book-overview.png?enhanced';
	import booksPic from '$lib/images/books-overview.jpg?enhanced';
	import librariesPic from '$lib/images/libraries-overview.png?enhanced';
	import libraryPic from '$lib/images/library-overview.png?enhanced';
	import contributorCliff from '$lib/images/contributor-cliff-chew.jpg?enhanced';
	import contributorBryan from '$lib/images/contributor-bryan-wong.jpg?enhanced';
	import contributorTingfeng from '$lib/images/contributor-tingfeng-wu.jpg?enhanced';

	import { goto } from '$app/navigation';
	import type { PageData } from './$types';

	const heroImages = [librariesPic, bookPic, booksPic, libraryPic];
	let { data }: { data: PageData } = $props();
	$effect(() => {
		if (data.session != null) {
			goto('/dashboard');
		}
	});
</script>

<svelte:head>
	<title>SG Lib Books</title>
</svelte:head>

<Header user={data.user} />
<main class="">
	<!-- Hero header -->
	<section
		id="hero"
		class="min-h-[85vh] bg-gradient-to-b from-slate-100 to-white container-sm md:container-lg md:mx-auto px-5 text-xl font-primary"
	>
		<div class="mx-auto text-center py-16 max-w-3xl">
			<h1 class="mb-6 text-5xl md:text-6xl font-semibold text-slate-700">
				Redefining your book borrowing experience
			</h1>
			<p class="text-slate-500 mb-8">
				<!-- Find out which libraries have the books you want. Get notified when they are available for -->
				<!-- loan. -->
				Borrowing your favourite books easier at your neighbourhood public libraries
			</p>
			<Button href="/dashboard" class="ml-auto mb-10">
				<LogIn class="mr-2 h-4 w-4" />
				<span>Try out now!</span>
			</Button>
			<Carousel.Root
				class="mb-10 shadow-lg shadow-slate-500 rounded-xl"
				opts={{ loop: true }}
				plugins={[Autoplay({ delay: 3000 })]}
			>
				<Carousel.Content class="rounded-xl">
					{#each heroImages as highlightPic}
						<Carousel.Item class="rounded-xl">
							<enhanced:img class="rounded-xl" src={highlightPic} alt="sg-lib-books" />
						</Carousel.Item>
					{/each}
				</Carousel.Content>
				<Carousel.Previous />
				<Carousel.Next />
			</Carousel.Root>
		</div>
	</section>
	<section class="container my-6">
		<div class="flex lg:flex-row flex-col items-center lg:gap-16 gap-3">
			<div class="w-72 flex flex-col gap-3 mb-9">
				<div class="flex items-center">
					<Library class="mr-4 w-6 h-6" />
					<h3 class="text-2xl font-semibold">Library View</h3>
				</div>
				<p class="text-slate-700">
					<!-- Check out the books availibility on each library. You wont missed out your favourite books -->
					<!-- on-shelve again! -->
					Instant view of books availability across libraries in a single page—no more endless clicks!
				</p>
			</div>
			<div class="w-72 flex flex-col gap-3 mb-9">
				<div class="flex items-center">
					<Radar class="mr-4 w-6 h-6" />
					<h3 class="text-2xl font-semibold">Plan your Trip Ahead</h3>
				</div>
				<p class="text-slate-700">
					<!-- Know which library has your favourite books so you can plan your journey ahead. -->
					Heading to the library? Quickly check which books are available for borrowing nearby!
				</p>
			</div>
			<div class="w-72 flex flex-col gap-3 mb-9">
				<div class="flex items-center">
					<Smartphone class="mr-4 w-6 h-6" />
					<h3 class="text-2xl font-semibold">Mobile Friendly</h3>
				</div>
				<p class="text-slate-700">
					<!-- Easily check the availability of your favorite books anytime, anywhere, on any device. -->
					Your perfect library companion—accessible anytime, anywhere on your mobile phone!
				</p>
			</div>
			<div class="w-72 flex flex-col gap-3 mb-9">
				<div class="flex items-center">
					<Sprout class="mr-4 w-6 h-6" />
					<h3 class="text-2xl font-semibold">Community Driven</h3>
				</div>
				<p class="text-slate-700">
					From fellow readers to the community, we're here to tackle the pain points that bugs us
					too.
				</p>
			</div>
		</div>
	</section>
	<section class="container mb-9 flex flex-col md:flex-row gap-6">
		<div class="flex items-center">
			<div>
				<h2 class="mb-6 text-4xl font-semibold text-slate-700">
					Calling all Singapore library users!
				</h2>
				<p class="text-slate-700 text-lg mb-3">
					Tired of always missing out on your favorite books at the library? We've got you covered!
				</p>
				<ul class="text-slate-700 text-lg">
					<li><span class="mr-3">📚</span> Bookmark your favourite titles</li>
					<li><span class="mr-3">📍</span> Discover which libraries have the books you love</li>
					<li><span class="mr-3">🔔</span> Get notified when they're available</li>
					<li><span class="mr-3">🚀</span> More exciting features are on the way!</li>
				</ul>
			</div>
		</div>
		<div class="rounded-xl max-w-sm mx-auto">
			<img class="rounded-xl" src={readingPic} alt="reading animated icons" />
		</div>
	</section>
	<section class="bg-gradient-to-b from-white to-slate-100" id="about-us">
		<div class="max-w-6xl mx-auto text-center px-3">
			<h2 class="mb-6 text-4xl font-semibold text-slate-700">About Us</h2>
			<p class="text-slate-700 mb-10 text-lg max-w-4xl mx-auto">
				<!-- We are a group of Singapore tech and book enthusiasts who want to improve our library tech experience! -->
				We are a group of Singapore tech and book enthusiasts who wanted to improve our physical library
				book borrowing experience.
			</p>
			<div class="grid md:grid-cols-4 grid-cols-2 gap-3 md:gap-10 pb-20">
				<div class="flex flex-col gap-1 p-5">
					<enhanced:img
						src={contributorCliff}
						alt="Cliff Chew"
						class="rounded-full p-3 border-slate-200"
					/>
					<h3 class="text-slate-900 text-lg">Cliff Chew</h3>
					<div class="flex justify-center">
						<Button variant="ghost" href="https://www.linkedin.com/in/cliff-chew-kt/"
							><Linkedin class="w-5 h-5" /></Button
						>
						<Button variant="ghost" href="https://github.com/cliffchew84"
							><Github class="w-5 h-5" /></Button
						>
					</div>
				</div>
				<div class="flex flex-col gap-1 p-5">
					<enhanced:img
						src={contributorBryan}
						alt="Bryan Wong"
						class="rounded-full p-3 border-slate-200"
					/>
					<h3 class="text-slate-900 text-lg">Bryan Wong</h3>
					<div class="flex justify-center">
						<Button variant="ghost" href="https://www.linkedin.com/in/zw-wong/"
							><Linkedin class="w-5 h-5" /></Button
						>
						<Button variant="ghost" href="https://github.com/kiritowu"
							><Github class="w-5 h-5" /></Button
						>
					</div>
				</div>
				<div class="flex flex-col gap-1 p-5">
					<enhanced:img
						src={contributorTingfeng}
						alt="Tingfeng Wu"
						class="rounded-full p-3 border-slate-200"
					/>
					<h3 class="text-slate-900 text-lg">Tingfeng Wu</h3>
					<div class="flex justify-center">
						<Button variant="ghost" href="https://www.linkedin.com/in/wutingfeng/"
							><Linkedin class="w-5 h-5" /></Button
						>
						<Button variant="ghost" href="https://github.com/elliotwutingfeng"
							><Github class="w-5 h-5" /></Button
						>
					</div>
				</div>
				<div class="flex flex-col gap-1 p-5">
					<div class="rounded-full p-3 border-slate-200 border">
						<Github class="w-24 h-24 md:w-36 md:h-36 md:m-6 mx-auto" />
					</div>
					<h3 class="text-slate-900 text-lg">
						Join our <a
							href="https://github.com/cliffchew84/SG-Lib-Books"
							class="underline font-semibold">open-source</a
						> community!
					</h3>
				</div>
			</div>
		</div>
	</section>
	<section class="bg-gradient-to-b from-slate-100 to-slate-50" id="waitlist">
		<div class="max-w-3xl mx-auto text-center">
			<h2 class="mb-6 text-4xl font-semibold text-slate-700">Join our waitlist!</h2>
			<p class="text-slate-600 mb-8 text-lg">
				Love what we are doing? Receives an email from us as soon as our web application is ready
				for everyone.
			</p>
			<Button class="mb-10" href="https://forms.gle/C4MyKxAyUhhgds4U9">
				<LogIn class="mr-2 h-4 w-4" />
				<span>Join Our Waitlist!</span>
			</Button>
			<p class="text-slate-600 pt-8 pb-1 text-sm">
				SG Lib Books is an independent project that has no affiliation with the National Library
				Board.
			</p>
			<p class="text-slate-600 pb-2 text-sm">
				Data displayed by SG Lib Books is licensed under the <a
					href="https://data.gov.sg/open-data-licence"
					class="underline">Singapore Open Data Licence</a
				>.
			</p>
			<p class="text-slate-600 pb-2 text-sm">
				<a
					href="https://www.flaticon.com/free-animated-icons/reading"
					title="reading animated icons">Reading animated icons created by Freepik - Flaticon</a
				>
			</p>
		</div>
	</section>
</main>
<Footer />
