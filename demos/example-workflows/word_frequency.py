from nltk.corpus import inaugural
import re
import pickle
import matplotlib.pyplot as plt

X_TICK_FREQUENCY = 6

def calculate_frequency_map(word_list):
    frequency_map = {}
    for word in word_list:
        word = word.lower()
        frequency_map[word] = frequency_map.get(word, 0) + 1
    return frequency_map

def generate_plot(word, maps):
    keys = [k for k in maps.keys()]
    keys.sort()
    y = [maps[k].get(word.lower(), 0) for k in keys]
    
    plt.plot(keys, y)
    plt.ylabel("Frequency")
    plt.xlabel("Year")
    plt.title("Frequency Per Year of '" + word + "'")

    locs, labels = plt.xticks()
    plt.xticks(locs[::-X_TICK_FREQUENCY])

    plt.show()

# @BEGIN main
# @IN inaugural @@URI file:data/inaugural.zip
# @IN search_word
# @OUT pkl @URI file:data/norm_addresses.pkl
# @OUT frequency_maps
def main():
    # @BEGIN normalize_list
    # @IN inaugural @URI file:data/inaugural.zip
    # @OUT normalized_addresses 
    file_ids = inaugural.fileids()
    print(file_ids)
    normalized_addresses = []
    for address in file_ids:
        normalized_words = [address.split("-")[0]]
        for sent in inaugural.sents(address):
            prev_word = ""
            for word in sent:
                if(prev_word == "'"):
                    continue
                
                normalized = re.sub("[^a-z0-9]", "", word.lower())
                if(normalized != ""):
                    normalized_words.append(normalized)
                prev_word = word
        normalized_addresses.append(normalized_words)
    # @END normalized_list

    # @BEGIN pickleize
    # @IN normalized_addresses
    # @OUT pkl @URI file:data/norm_addresses.pkl
    fout = open("norm_addresses.pkl", "wb")
    pickle.dump(normalized_addresses, fout)
    fout.close()
    # @END pickleize

    # deserialize pkl file
    # @BEGIN depickleize
    # @IN pkl @URI file:data/norm_addresses.pkl
    # @OUT address_word_list
    fin = open("norm_addresses.pkl", "rb")
    address_word_list = pickle.load(fin)
    fin.close()
    # @END depickleize

    # @BEGIN frequency
    # @IN address_word_list
    # @IN search_word
    # @OUT frequency_maps
    search_word = input("Input word to find frequency: ")


    frequency_maps = {}
    for word_list in address_word_list:
        
        frequency_maps[word_list[0]] = calculate_frequency_map(word_list[1:])
    # @END frequency
    

    generate_plot(search_word, frequency_maps)
# @END main


if __name__ == "__main__":
    main()
