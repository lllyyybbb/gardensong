# gardensong
poems from my urban garden in baltimore city.

# dispatches from my little "bump in the earth" (to quote poet Tyree Daye)

*Poems generated from data from a sensor that Markov-writes a poem every hour, in the voices of Black poets from the public domain.*

<img width="535.5" height="714" alt="sensor" src="https://github.com/user-attachments/assets/60b6fcf8-92ca-46c8-b924-4b942af81a1e" />


A small dht11 sensor attached to an adafruit feather huzzah sits out among the plants, running on a solar-charged battery. It wakes with the light and, at the top of each hour through the day, reads the air around it —
temperature and humidity — and turns those two numbers into a poem, published here.
After dark, on its spent battery, it sleeps until morning.
The garden's environment is transliterated into poetry. 

Each poem is assembled, word by word, by a Markov chain (order of 2)
drawing only on public-domain poetry by Black poets of the late nineteenth and
early twentieth centuries.

## How the sensor readings shape the poem

Two numbers become the poem's form:

- **Humidity** sets its length — about one line for every ten percent. In theory, a damp
  morning writes a long poem; dry air, a short one.
- **Temperature** sets how far the lines stretch and how wild the language runs.
  Cool air keeps close to the poets' most worn phrasings. Warm
  air lets rarer, stranger words rise to the surface — loose, molten.

The temperature is also the random seed for the Markov chain, 
so the same reading always yields the same poem, 
so each one is the trace of a single moment in the garden. 
A new poem appears at the top of every hour; the ones before
it are kept below.

## Sources

All text is drawn from two public-domain volumes, digitized by
[Project Gutenberg](https://www.gutenberg.org):

- ***The Book of American Negro Poetry***, chosen and edited by James Weldon
  Johnson (1922) — the first anthology of its kind, gathering thirty-one poets.
-***Harlem Shadows*** by Claude McKay
-***Poems*** by Frances E. W. Harper
### The poets

From Johnson's anthology: Paul Laurence Dunbar · James Edwin Campbell ·
James D. Corrothers · Daniel Webster Davis · William H. A. Moore · W. E. B. Du Bois ·
George Marion McClellan · William Stanley Braithwaite · George Reginald Margetson ·
James Weldon Johnson · John Wesley Holloway · Leslie Pinckney Hill ·
Edward Smyth Jones · Ray G. Dandridge · Fenton Johnson · R. Nathaniel Dett ·
Georgia Douglas Johnson · Claude McKay · Joseph S. Cotter Jr. · Roscoe C. Jamison ·
Jessie Fauset · Anne Spencer · Alex Rogers · Waverley Turner Carmichael ·
Alice Dunbar-Nelson · Charles Bertram Johnson · Otto Leyland Bohanan ·
Theodore Henry Shackelford · Lucian B. Watkins · Benjamin Brawley ·
Joshua Henry Jones Jr.

All source poems are in the U.S. public domain; the poems generated here are free
to read and share.

## Note: 
While period-specific uses of the n-word may be in the corpus, they are not pushed to the public site (a choice made by me.)
Period-specific uses of the word "Negro" are included. 

## How it's made

A dht11 sensor + adafruit feather huzzah + 3.7v LiPo battery + solar panel at the plants, a Raspberry Pi inside running a Markov chain and connecting to 
a Grafana dash. A new poem is generated and published on the hour when the board is awake.

Assisted by Claude Code and the Adafruit docs. 
