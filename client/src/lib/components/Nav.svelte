<script lang="ts">
	import daisyuiColors from 'daisyui/src/theming/themes';
	import Icon from '@iconify/svelte';
	import { selectedTheme } from '$lib/store';
	import { onMount } from 'svelte';

	let themes = Object.keys(daisyuiColors);

	// Read the selected theme from local storage or cookies when the component mounts
	onMount(() => {
		const storedTheme = localStorage.getItem('selectedTheme');
		if (storedTheme && themes.includes(storedTheme)) {
			selectedTheme.set(storedTheme);
			document.documentElement.setAttribute('data-theme', storedTheme);
		}
	});

	// Function to handle theme selection
	function handleThemeChange(event: any) {
		const theme = event.target.value;
		selectedTheme.set(theme);
		// Save the selected theme to local storage or cookies
		localStorage.setItem('selectedTheme', theme);
	}
</script>

<div class="bg-base-300 sticky top-0 -z-[-1] shadow">
	<div class="navbar bg-base-300 mx-auto flex max-w-2xl justify-between gap-2">
		<div class="">
			<a href="/" class="btn btn-primary flex items-center text-xl">
				<Icon icon="fa6-solid:poop" class="h-7 w-7" />
				<div class="flex items-start gap-1">
					<div>Kitty Crapper</div>
					<!-- <div class="text-xs">beta</div> -->
				</div>
			</a>
		</div>

		<!-- <div class="flex items-center gap-2 w-full sm:w-1/2 lg:w-1/3"> -->
		<!-- <div class="form-control w-full"> -->
		<!-- <input type="text" placeholder="Search" class="input input-bordered focus:outline-none" /> -->
		<!-- </div> -->

		<!-- <div> -->
		<!-- <button class="btn btn-primary">Search</button> -->
		<!-- </div> -->
		<!-- </div> -->

		<div class="">
			<div class="dropdown dropdown-end">
				<div tabindex="0" role="button">
					<div class="lg:tooltip lg:tooltip-left" data-tip="Theme Selector">
						<button class="btn btn-ghost">
							<div class="font-normal lowercase">
								<Icon icon="gridicons-themes" class="h-7 w-7" />
							</div>
						</button>
					</div>
				</div>
				<ul
					tabindex="-1"
					class="dropdown-content dropdown-end rounded-box border-primary bg-base-100 -z-[-1] mt-3 h-96 w-52 overflow-auto border p-2 shadow"
				>
					{#each themes.sort() as theme}
						<li>
							<input
								type="radio"
								name="theme-dropdown"
								class="theme-controller btn btn-ghost btn-sm btn-block justify-start font-medium"
								aria-label={theme}
								value={theme}
								on:change={handleThemeChange}
							/>
						</li>
					{/each}
				</ul>
			</div>

			<!-- <div class="dropdown dropdown-end">
				<div tabindex="0" role="button" class="avatar btn btn-circle btn-ghost">
					<div class="w-10 rounded-full border border-primary">
						<img
							alt="Tailwind CSS Navbar component"
							src="https://daisyui.com/images/stock/photo-1534528741775-53994a69daeb.jpg"
						/>
					</div>
				</div>

				<ul
					class="menu dropdown-content menu-sm z-[1] mt-3 w-52 rounded-box border border-primary bg-base-100 p-2 shadow"
				>
					<li>
						<a href="/" class="justify-between">
							Profile
							<span class="badge">New</span>
						</a>
					</li>
					<li><a href="/">Settings</a></li>
					<li><a href="/">Logout</a></li>
				</ul>
			</div> -->
		</div>
	</div>
</div>
