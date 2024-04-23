<script lang="ts">
	import { fade, slide } from 'svelte/transition';
	import kona from '$lib/assets/images/kona.png';
	import whiskerImg from '$lib/assets/images/whisker.png';
	import { onMount } from 'svelte';
	import Icon from '@iconify/svelte';
	import Stats from '$lib/components/Stats.svelte';

	let dump: any;
	let status: any;
	let activity: any;
	let clean: any;

	const getDump = async () => {
		const res = await fetch('/api/dump');
		dump = await res.json();
		console.log(dump);
		return dump;
	};

	const getStatus = async () => {
		const res = await fetch('/api/status');
		status = await res.json();
		console.log(status);
		return status;
	};

	const getActivity = async () => {
		const res = await fetch('/api/activity');
		activity = await res.json();
		console.log(activity);
		return activity;
	};

	const startClean = async () => {
		const res = await fetch('/api/clean');
		clean = await res.json();
		console.log(clean);
		return clean;
	};

	onMount(() => {
		getDump();
		getStatus();
		// getActivity();
	});
</script>

<div class="mx-auto w-full max-w-2xl px-2 py-10">
	<div class=" flex w-full flex-col gap-5 md:flex-row">
		<div class="relative mx-auto flex w-1/2 items-center justify-center">
			<div class="flex flex-col items-center gap-2">
				{#if dump?._data?.name}
					<div in:fade={{ delay: 0, duration: 500 }} class="text-primary text-2xl font-bold">
						{dump?._data?.name}
					</div>
				{:else}
					<div in:fade={{ delay: 0, duration: 500 }} class="text-primary text-2xl font-bold">
						Robot
					</div>
				{/if}
				<img src={whiskerImg} alt="whisker" class="object-scale-down" />

				{#if dump?._data?.isOnline}
					<div class="badge badge-lg bg-base-300 flex items-center gap-2 py-4">
						<div class="bg-success h-5 w-5 rounded-full shadow-lg"></div>
						<div>Online</div>
					</div>
				{:else}
					<div class="badge badge-lg bg-base-300 flex items-center gap-2 py-4">
						<div class="loading loading-spinner loading-sm"></div>
						<div>Loading...</div>
					</div>
				{/if}
			</div>
		</div>

		<div class="card flex w-full flex-col gap-2">
			<div class="h-full w-full">
				<Stats
					data={{
						status: status,
						catWeight: dump?._data?.catWeight,
						litterLevel: dump?._data?.DFILevelPercent + '%',
						weightSensor: dump?._data?.weightSensor + ' lbs',
						weightEnabled: dump?._data?.smartWeightEnabled
							? 'Weight sensor is enabled'
							: 'Weight sensor is disabled',
						litterFull: dump?._data?.isDFIFull ? 'Litter box is full' : 'Litter box is not full',
						catDetect: dump?._data?.catDetect
					}}
				/>
			</div>
		</div>
	</div>

	<!-- <h1 class="text-primary py-2 text-2xl font-thin">Actions</h1> -->
	<div class="my-10 grid grid-cols-2 gap-2 sm:grid-cols-2 lg:grid-cols-4">
		<button
			on:click={startClean}
			class="btn btn-primary flex w-full items-center justify-between gap-2"
		>
			<div>Clean</div>
			<Icon icon="akar-icons:arrow-cycle" class="h-5 w-5" />
		</button>
		<div class="btn btn-primary flex w-full items-center justify-between gap-2">
			<div>Light</div>
			<Icon icon="material-symbols:lightbulb-rounded" class="h-5 w-5" />
		</div>
		<div class="btn btn-primary flex w-full items-center justify-between gap-2">
			<div>Status</div>
			<Icon icon="material-symbols:info" class="h-5 w-5" />
		</div>
		<div class="btn btn-primary flex w-full items-center justify-between gap-2">
			<div>Activity</div>
			<Icon icon="tdesign:activity" class="h-5 w-5" />
		</div>
	</div>

	<div class="my-10 flex w-full snap-x snap-mandatory gap-2 overflow-x-auto">
		<div class="card bg-base-300 snap-center">
			<div class="card-body w-72">
				<div class="flex h-full items-center gap-5">
					<div class="avatar">
						<div class="border-primary w-16 rounded-full border shadow">
							<img src={kona} alt="kitty" class="" />
						</div>
					</div>
					<div class="card-title">I took 37 💩.</div>
				</div>
			</div>
		</div>

		<div class="card bg-base-300 snap-center">
			<div class="card-body w-72">
				<div class="flex h-full items-center gap-5">
					<div class="avatar">
						<div class="border-primary w-16">
							<!-- <img src={kona} alt="kitty" class="" /> -->
							<Icon icon="tabler:shovel" class="text-primary h-full w-full" />
						</div>
					</div>
					<div class="card-title text-base">
						{dump?._data?.scoopsSavedCount || 'loading...'} scoops saved since using {dump?._data
							?.name}
					</div>
				</div>
			</div>
		</div>

		<div class="card bg-base-100 image-full snap-center shadow-xl">
			<figure class="bg-primary h-full">
				<img src={whiskerImg} alt="Shoes" class="max-h-40 object-cover" />
			</figure>
			<div class="card-body w-72">
				<h2 class="card-title">Shoes!</h2>
				<p>If a dog chews shoes whose shoes does he choose?</p>
				<!-- <div class="card-actions justify-end"> -->
				<!-- <button class="btn btn-primary">Buy Now</button> -->
				<!-- </div> -->
			</div>
		</div>

		<div class="card bg-primary text-primary-content snap-center">
			<div class="card-body w-72">
				<div class="flex h-full flex-col items-start gap-2">
					<h2 class="card-title">Card title!</h2>
					<p>If a dog chews shoes whose shoes does he choose?</p>
					<!-- <div class="card-actions justify-end"> -->
					<!-- <button class="btn">Buy Now</button> -->
					<!-- </div> -->
				</div>
			</div>
		</div>
	</div>

	<!-- {#if activity}
		{#each activity as act}
			<div class="card">
				<div class="card-body">
					{act.timestamp}
					{act.action}
				</div>
			</div>
		{/each}
	{:else}
		<div class="loading loading-lg"></div>
	{/if} -->
</div>
