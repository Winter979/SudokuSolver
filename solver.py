
class Solver:
   def begin_simple(self, array, shape="row"):
      values_left = [1,2,3,4,5,6,7,8,9]
      values_done = []
      remaining = 9

      unknown = []


      for cell in array:
         value = cell.getValue()
         if value != 0:
            try:
               values_left.remove(value)
            except ValueError:
               print("="*80)
               print(values_left)
               print("TRIED REMOVING:", value)
            
            values_done.append(value)
            remaining -=1
         else:
            unknown.append(cell)
            # The value has already been found
            pass

      if remaining == 0:
         # This section is complete
         pass
      else:
         for cell in unknown:
            for value in values_done:
               cell.remove_number(value)
         self.find_solos(unknown, remaining)
         # self.find_subset(unknown, remaining)
         
   def find_solos(self,unknown, remaining):

      combined = []

      for cell in unknown:
         combined.extend(cell.numbers)

      solos = []

      for ii in range(1,10):
         if combined.count(ii) == 1:
            solos.append(ii)

      for value in solos:
         for cell in unknown:
            if value in cell.numbers:
               cell.setValue(value)

   def find_subset(self, array, remaining):
      subsets = []
      for cell in array:
         if cell.value == 0:
            subsets.append(cell.numbers)

      subset_count = len(subsets)

      # Direct subsets

      for subset in subsets:
         length = len(subset)
         count = subsets.count(subset)

         if count == length:
            for ii in range(subset_count):
               if subset != subsets[ii]:
                  for number in subset:
                     array[ii].remove_number(number)
                     
      # Indirect subsets

      # for ii in range(subset_count):
      #    subset = subsets[ii]
      #    length = len(subset)

      #    partial_matches = 1
      #    matches_list = []
      #    matches_list.append(ii)

      #    for jj in range(subset_count):

      #       if ii != jj:
      #          subset2 = subsets[jj]
      #          match = False
      #          for value in subset:
      #             if value in subset2:
      #                match  = True
               
      #          if match:
      #             partial_matches += 1
      #             matches_list.append(jj)

      #    if partial_matches == length:

      #       print("PARTIAL MATCHES:", partial_matches, subset)

      #       other_values = [1,2,3,4,5,6,7,8,9]

      #       for value in subset:
      #          other_values.remove(value)

      #       for kk in range(subset_count):
      #          if kk in matches_list:
      #             for value in other_values:
      #                array[kk].remove_number(value)
      #          else:
      #             for value in subset:
      #                array[kk].remove_number(value)
            

   def generate_subset(self,cell):
      subset_array = []
      for number in cell.numbers:
         if number != 0:
            subset_array.append(number)
            
      return int(''.join(subset_array))


   