<script lang="ts">
	import { fade, slide } from 'svelte/transition';
	import kona from '$lib/assets/images/kona.png';
	import whiskerImg from '$lib/assets/images/whisker.png';
	import { onMount, onDestroy } from 'svelte';
	import Icon from '@iconify/svelte';
	import Stats from '$lib/components/Stats.svelte';

	import { PUBLIC_WEB_SOCKET_URL } from '$env/static/public';

	let ws: WebSocket;

	type EndpointKey = 'dump' | 'robots' | 'status';

	const endpoints: Record<EndpointKey, string> = {
		dump: '/api/dump',
		robots: '/api/robots',
		status: '/api/status'
	};

	let data: Record<EndpointKey, any> = {
		dump: null,
		robots: null,
		status: null
	};

	const fetchData = async (key: EndpointKey) => {
		const res = await fetch(endpoints[key]);
		data[key] = await res.json();
	};

	const fetchDataForAllKeys = () => {
		Object.keys(endpoints).forEach((key) => fetchData(key as EndpointKey));
	};

	let clean: any;
	let isCleaning = false;

	const startClean = async () => {
		isCleaning = true;
		const res = await fetch('/api/clean');
		clean = await res.json();
		// console.log(clean);
		return clean;
	};

	onMount(() => {
		fetchDataForAllKeys();

		setTimeout(() => {
			ws = new WebSocket(PUBLIC_WEB_SOCKET_URL);
			ws.onmessage = (event) => {
				const newData = JSON.parse(event.data);
				Object.keys(newData).forEach((key) => {
					data[key as keyof typeof data] = newData[key as keyof typeof newData];
				});
			};

			ws.onerror = (error) => {
				console.error('WebSocket error:', error);
			};

			ws.onclose = () => {
				console.log('WebSocket connection closed');
			};
		}, 5000); // 5-second delay
	});

	onDestroy(() => {
		if (ws) {
			ws.close();
		}
	});
</script>

<!-- {JSON.stringify(data)} -->

<div class="mx-auto w-full max-w-2xl px-2 py-10">
	<div class=" flex w-full flex-col gap-5 md:flex-row">
		<div class="relative mx-auto flex w-1/2 items-center justify-center">
			<div class="flex flex-col items-center gap-2">
				{#if data?.dump?._data?.name}
					<div in:fade={{ delay: 0, duration: 500 }} class="text-primary text-3xl font-bold">
						{data?.dump?._data?.name}
					</div>
				{:else}
					<div in:fade={{ delay: 0, duration: 500 }} class="text-primary text-3xl font-bold">
						Robot
					</div>
				{/if}
				<div class="relative">
					<img src={whiskerImg} alt="whisker" class="object-scale-down" />
				</div>

				<!-- EASTER EGG 🐇🥚 -->

				{#if data?.status === 'ROBOT_CLEAN'}
					<div class="absolute top-28 -translate-y-8 sm:-translate-y-2">
						<img
							transition:fade={{ duration: 500 }}
							src={kona}
							alt="kitty"
							class="animate-spin-slow h-32 w-32 rounded-full shadow-lg"
						/>
					</div>
				{/if}
				{#if data?.dump?._data?.isOnline}
					<div class="badge badge-lg bg-base-300 flex items-center gap-2 py-4">
						<div class="bg-success h-5 w-5 rounded-full shadow-lg"></div>
						<div>Online</div>
					</div>
				{:else}
					<div class="badge badge-lg bg-base-300 flex items-center gap-2 py-4">
						<div class="bg-error h-5 w-5 rounded-full shadow-lg"></div>
						<div>Offline</div>
					</div>
				{/if}
			</div>
		</div>

		<div class="card flex w-full flex-col gap-2">
			<div class="h-full w-full">
				<Stats
					data={{
						status: data?.status,
						catWeight: data?.dump?._data?.catWeight,
						litterLevel: data?.dump?._data?.DFILevelPercent + '%',
						weightSensor: data?.dump?._data?.weightSensor + ' lbs',
						weightEnabled: data?.dump?._data?.smartWeightEnabled
							? 'Weight sensor is enabled'
							: 'Weight sensor is disabled',
						litterFull: data?.dump?._data?.isDFIFull
							? 'Litter box is full'
							: 'Litter box is not full',
						catDetect: data?.dump?._data?.catDetect
					}}
				/>
			</div>
		</div>
	</div>

	<!-- <h1 class="text-primary py-2 text-2xl font-thin">Actions</h1> -->
	<div class="my-10 grid grid-cols-2 gap-2 sm:grid-cols-2 lg:grid-cols-4">
		<button
			on:click={startClean}
			class="btn btn-primary btn-lg flex w-full items-center justify-between gap-2"
		>
			{#if isCleaning && data?.status !== 'ROBOT_CLEAN'}
				<div>Starting</div>
			{:else}
				<div>Clean</div>
			{/if}
			<!-- {/if} -->

			<!-- {isCleaning} -->

			{#if data?.status === 'ROBOT_CLEAN' ? () => (isCleaning = false) : ''}
				<div class="animate-spin-slow">
					<Icon icon="akar-icons:arrow-cycle" class="h-7 w-7" />
				</div>
			{:else}
				<Icon icon="akar-icons:arrow-cycle" class="h-7 w-7" />
			{/if}
			<!-- <Icon icon="akar-icons:arrow-cycle" class="h-5 w-5" /> -->
		</button>
		<div class="btn btn-primary btn-lg flex w-full items-center justify-between gap-2">
			<div>Light</div>
			<Icon icon="material-symbols:lightbulb-rounded" class="h-7 w-7" />
		</div>
		<div class="btn btn-primary btn-lg flex w-full items-center justify-between gap-2">
			<div>Status</div>
			<Icon icon="material-symbols:info" class="h-7 w-7" />
		</div>
		<div class="btn btn-primary btn-lg flex w-full items-center justify-between gap-2">
			<div>Activity</div>
			<Icon icon="tdesign:activity" class="h-7 w-7" />
		</div>
	</div>

	<div class="my-10 flex w-full snap-x snap-mandatory gap-2 overflow-x-auto">
		<div class="card bg-base-300 snap-center">
			<div class="card-body w-full min-w-72">
				<div class="flex h-full items-center gap-5">
					<div class="avatar">
						<div class="border-primary bg-primary w-16 rounded-full border shadow">
							<img src={kona} alt="kitty" class="" />
						</div>
					</div>
					<div class="card-title">
						I took {data?.dump?._data?.DFINumberOfCycles} <span class="text-2xl">💩</span>.
					</div>
				</div>
			</div>
		</div>

		<div class="card bg-base-300 snap-center">
			<div class="card-body h-full min-w-72">
				<div class="flex h-full items-center gap-5">
					<!-- <div class="avatar"> -->
					<!-- <div class="border-primary w-16"> -->
					<!-- <img src={kona} alt="kitty" class="" /> -->
					<!-- <Icon icon="tabler:shovel" class="text-primary h-full w-full" /> -->
					<!-- </div> -->
					<!-- </div> -->
					<div class="card-title text-base">
						<div>
							<span class="text-primary text-2xl font-bold"
								>{data?.dump?._data?.scoopsSavedCount || 'loading...'}</span
							>
							scoops saved since using {data?.dump?._data?.name}
						</div>
					</div>
				</div>
			</div>
		</div>

		<div class="card bg-base-100 image-full snap-center shadow-xl">
			<figure class="bg-primary h-full">
				<img src={whiskerImg} alt="Shoes" class="max-h-40 object-cover" />
			</figure>
			<div class="card-body w-full min-w-72">
				<h2 class="card-title">Shoes!</h2>
				<p>If a dog chews shoes whose shoes does he choose?</p>
				<!-- <div class="card-actions justify-end"> -->
				<!-- <button class="btn btn-primary">Buy Now</button> -->
				<!-- </div> -->
			</div>
		</div>

		<div class="card bg-primary text-primary-content snap-center">
			<div class="card-body w-full min-w-72">
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

<!-- {#if data?.activity}
	{#each data?.activity as act}
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
