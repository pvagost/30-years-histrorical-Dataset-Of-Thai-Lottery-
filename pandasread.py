import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re

df = pd.read_html("https://www.myhora.com/lottery/stats.aspx?mx=09&vx=30&rx=0")

#see the beheviour of the list
print("Length of Dataframe: ", len(df)) 
# for i, dff in enumerate(df): #understand the chareterisric of each table, enumerate gives index for each item
#     print(f"\n--- Table {i} ---")
#     print(f"Shape: {dff.shape}")
#     print("Columns:", dff.columns.tolist())
#     print(dff.head(3))

df_merge = df.copy() #copy df into new dataframe to keep df original

#merge incomplete tables
df_merge[1] = pd.concat([df_merge[1], df_merge[2]], ignore_index=True)
df_merge[8] = pd.concat([df_merge[8], df_merge[9]], ignore_index=True)
df_merge[15] = pd.concat([df_merge[15], df_merge[16]], ignore_index=True)
df_merge[22] = pd.concat([df_merge[22], df_merge[23]], ignore_index=True)
df_merge[29] = pd.concat([df_merge[29], df_merge[30]], ignore_index=True)

#delete after merging
delete_tables = [2, 9, 16, 23, 30, 35] #not interested in table35
for i in sorted(delete_tables, reverse=True):
    if i < len(df_merge):
        del df_merge[i]

# check data after arranging tables
print("Length of Merged Dataframe: ", len(df_merge))
# for i, dff in enumerate(df_merge): 
#     print(f"\n--- Table {i} ---")
#     print(f"Shape: {dff.shape}")
#     print("Columns:", dff.columns.tolist())
#     print(dff.head(3))

df_arranged = df_merge.copy()

unknown_tables = [2,5,8,9,10,11,14,15,16,17,20,21,22,23,26,27,28,29]
for i in sorted(unknown_tables, reverse=True):
    if i < len(df_arranged):
        del df_arranged[i]

#check data after deleting unnessary tables
print("Length of Arranged Dataframe: ", len(df_arranged))
# for i, dff in enumerate(df_arranged): 
#     print(f"\n--- Table {i} ---")
#     print(f"Shape: {dff.shape}")
#     print("Columns:", dff.columns.tolist())
#     print(dff.head(3))

#create a map of thai words to english words
thai_to_eng = {
    'หลัก': 'Position',
    'ร้อย': 'Hundreds',
    'สิบ': 'Tens',
    'หน่วย': 'Unit',
    'รวม': 'Total',
    'ครั้ง': 'Times',
    'ไม่เคยออก': 'Never',
    'เลข 0': '0', 'เลข 1': '1', 'เลข 2': '2', 'เลข 3': '3',
    'เลข 4': '4', 'เลข 5': '5', 'เลข 6': '6', 'เลข 7': '7',
    'เลข 8': '8', 'เลข 9': '9'
}
df_translated = df_arranged.copy()

#sub thai words with english words
for i in range(len(df_translated)):
    df_translated[i] = df_translated[i].replace(thai_to_eng, regex=True)

# for i, dff in enumerate(df_translated): 
#     print(f"\n--- Table {i} ---")
#     print(f"Shape: {dff.shape}")
#     print("Columns:", dff.columns.tolist())
#     print(dff.head(3))

#check if all of words are in english
for i, dff in enumerate(df_translated): 
    print(f"\n--- Table {i} ---")
    print(f"Shape: {dff.shape}")
    print("Columns:", dff.columns.tolist())
    print(dff) #display every single data

#categorized the types of tables tgt
per_digit_tables = {
    "Per-digit Frequency of Top 2 digits from 1st prize": df_translated[0],
    "Per-digit Frequency of 2-digit Prize": df_translated[2],
    "Per-digit Frequency of Last 3 digits from 1st prize": df_translated[4],
    "Per-digit Frequency of First 3 digits from 1st prize": df_translated[6],
    "Per-digit Frequency of Separate 3-digit prizes": df_translated[8],
    "Per-digit Frequency of Front 3-digit prizes": df_translated[10],
}
full_number_tables = {
    "Full Number Frequency of Top 2 digits from 1st prize": df_translated[1],
    "Full Number Frequency of 2-digit Prize": df_translated[3],
    "Full Number Frequency of Last 3 digits from 1st prize": df_translated[5],
    "Full Number Frequency of First 3 digits from 1st prize": df_translated[7],
    "Full Number Frequency of Separate 3-digit prizes": df_translated[9],
    "Full Number Frequency of Front 3-digit prizes": df_translated[11],
}

# plot for per-digit
fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(18, 18)) #create 3*2 grid and set the overall figure to size 18*18
fig.suptitle("Per-digit Frequency in Thai Lottery Tables", fontsize=18, y=0.98) #give a name with its size
axs = axs.flatten() #breakdown 2d array into 1d

for i, (title, df_translated) in enumerate(per_digit_tables.items()):
    # make a copy to avoid modifying the original data
    plot_df = df_translated.copy() 
    # set up the plot
    x = np.arange(10)  # use np to create x-axis array (0-9 digits)
    bar_width = 0.2
    axs[i].set_title(title, pad=10)  #sets the subplot title with 10 pixels of padding
    # track rows for positioning
    valid_rows = [] #track what is actual data not heading
    position_offset = 0
    # for each row, plot a bar for each digit
    for j, row_idx in enumerate(plot_df.index):
        if plot_df.iloc[j, 0] == 'Position':  # set if statement to skip header rows and 
            continue
        
        position = plot_df.iloc[j, 0]  # get position name and store like tens, unit, and so on
        valid_rows.append(j)
        # create a properly aligned array for all digits 0-9
        values = []
        for digit in range(10):
            # convert column value to proper format
            try:
                # get value directly from the digit column
                digit_value = plot_df.iloc[j, digit + 1]  # +1 because first column is position
                values.append(float(digit_value))
            except (IndexError, ValueError, TypeError):
                # if there is any error, it will try alternative methods
                try:
                    # try to find by column name
                    digit_col = str(digit)
                    if digit_col in plot_df.columns:
                        digit_value = plot_df.loc[j, digit_col]
                        values.append(float(digit_value))
                    else:
                        values.append(0)
                except (ValueError, TypeError, KeyError):
                    values.append(0)
        
        # position the bars properly
        axs[i].bar(x + position_offset * bar_width, values, width=bar_width, label=position)
        position_offset += 1
    
    # set the x-axis to show digits 0-9
    axs[i].set_xticks(x + bar_width * (len(valid_rows) - 1) / 2)
    axs[i].set_xticklabels([str(d) for d in range(10)])
    axs[i].set_xlabel("Digit", labelpad=10)
    axs[i].set_ylabel("Frequency")
    
    # show only rows that were actually plotted
    if valid_rows:
        axs[i].legend(title="Position")

plt.subplots_adjust(
    top=0.9,
    bottom=0.1,
    hspace=0.4,
    wspace=0.2,
    left=0.05,
    right=0.95
)
plt.tight_layout(rect=[0, 0, 1, 0.95], h_pad=2.5, w_pad=1.0)
plt.show()

#plot of full number histogram
fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(18, 18))
fig.suptitle("Full Number Frequency Distribution in Thai Lottery Tables", fontsize=18, y=0.98)
axs = axs.flatten()

for i, (title, table) in enumerate(full_number_tables.items()):
    # create a full list of (number, times) pairs
    data = []

    for idx, row in table.iterrows():
        times_label = row[0] #get labal from first column which is ___ times
        numbers = str(row[1]).split() if not pd.isna(row[1]) else [] #get numbers from 2nd column and create empty list if empty
        if times_label == "Never": #see never set to 0
            times = 0
        else:# extract number of times from text like 4 Times, 3 Times, convert to int
            match = re.match(r'(\d+)', times_label)
            times = int(match.group(1)) if match else None
        if times is not None: #successfully extracted, adds it to the data list for each number in this row
            for number in numbers:
                data.append(times)

    axs[i].hist(data, bins=range(0, max(data)+2), align='left', edgecolor='black', rwidth=0.8)
    axs[i].set_title(title, pad=10)
    axs[i].set_xlabel("Times Appeared")
    axs[i].set_ylabel("Number of Numbers")
    axs[i].set_xticks(range(0, max(data)+1))

plt.tight_layout(rect=[0, 0, 1, 0.95], h_pad=2.5, w_pad=1.0)
plt.show()
